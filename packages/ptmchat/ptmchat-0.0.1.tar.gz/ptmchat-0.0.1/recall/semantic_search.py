# 语义检索召回
import numpy as np
import requests
import json
from sklearn.decomposition import IncrementalPCA
import pickle
from tqdm import tqdm
import time
import os
import sys
import pandas as pd

sys.path.append("..")
import torch
from torch.utils.data.distributed import DistributedSampler
import argparse
import torch.backends.cudnn as cudnn
import faiss
from model.ernie import infer_batch, ErnieVectorizer
from data_loader.v1_data import Q2Dataset
from data_loader.v2_data import Q2StreamSubset


class FaissSearcher:
    def __init__(self, args, config):
        super().__init__()
        self.num_gpu = args.num_gpu
        self.batch_size = config['recall']['batch_size']
        self.max_seq_len = config['recall']['max_seq_len']
        # 候选文件
        self.candidate_file = config['inputs']['candidate_file']
        # 加载编码模型
        self.model = ErnieVectorizer()
        self.tokenizer = self.model.tokenizer
        # put model to GPU if available
        self.local_rank = args.local_rank
        torch.cuda.set_device(self.local_rank)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
            self.model = torch.nn.parallel.DistributedDataParallel(self.model,
                                                                   device_ids=[self.local_rank],
                                                                   output_device=self.local_rank,
                                                                   find_unused_parameters=True)

    def candidate_vectorize(self):
        """
        调用编码模型批量预测所有候选句子的特征向量，可分布式
        :return: 返回候选句子总数。向量保存为npy文件。
        """
        # 分布式训练，全量数据读取
        dataset = Q2Dataset(self.candidate_file)
        vecs = []
        with torch.no_grad():
            if torch.cuda.is_available():
                print('using pytorch DistributedSampler')
                sampler = DistributedSampler(dataset, shuffle=False)  # 只能兼容map style dataset
                loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, sampler=sampler,
                                                     pin_memory=True)
            else:
                loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=False,
                                                     pin_memory=True)
            for data in loader:
                vec = infer_batch(data,
                                  self.model,
                                  self.tokenizer,
                                  self.max_seq_len)
                if torch.cuda.is_available():
                    vec = vec.cpu()
                vecs.append(vec)
        vecs = torch.cat(vecs).numpy()
        if torch.cuda.is_available():
            np.save(f'candidates_part{self.local_rank}', vecs)
        else:
            np.save('candidates', vecs)

        assert len(dataset) <= vecs.shape[0] * self.num_gpu < len(dataset) + self.num_gpu, \
            f'num of vectors is {vecs.shape[0]}, but num of sentences is {len(dataset)}'
        return len(dataset)

    def vec_gen(self):
        """
        单进程vector生成器，从多个npy文件中轮流读取vector并流式生成。本身不控制生成结束。
        :return: yield一个vector
        """
        if torch.cuda.is_available():
            cycle = 0  # 轮数，用来同步遍历每个部分文件
            vec_all = []
            for i in range(self.num_gpu):
                vec_all.append(np.load(f'candidates_part{i}.npy', mmap_mode='r'))
            while 1:
                for i in range(self.num_gpu):
                    yield vec_all[i][cycle, :]
                cycle += 1
        else:
            vec_all = np.load('candidates.npy', mmap_mode='r')
            for i in range(vec_all.shape[0]):
                yield vec_all[i, :]

    def build_index(self, n_candidates):
        """
        构建faiss索引，仅单进程
        :param n_candidates: 候选总数
        :return: 索引
        """
        rows = []
        vecs = self.vec_gen()
        for i in range(n_candidates):
            rows.append(next(vecs))
        arr = np.stack(rows, axis=0).astype('float32')
        res = faiss.StandardGpuResources()  # use a single GPU
        dim = 768
        assert arr.shape == (n_candidates, dim)
        measure = faiss.METRIC_L2
        param = 'PCA128, IVF10000, PQ16'
        vec_index = faiss.index_factory(dim, param, measure)
        if torch.cuda.is_available():
            gpu_index = faiss.index_cpu_to_gpu(res, 0, vec_index)
            print(gpu_index.is_trained)
            gpu_index.train(arr)
            gpu_index.add(arr)
            print('total rows: ', gpu_index.ntotal)
            return gpu_index
        else:
            print(vec_index.is_trained)
            vec_index.train(arr)
            vec_index.add(arr)
            print('total rows: ', vec_index.ntotal)
            return vec_index

    def recall(self, query, index):
        """
        在faiss索引中检索
        :param query: 一批原始查询语句（不分词，仅q2）
        :param index: 索引
        :return:
        """
        index.nprobe = 10
        with torch.no_grad():
            q_vecs = infer_batch(query, self.model, self.tokenizer, self.max_seq_len)
            if torch.cuda.is_available():
                q_vecs = q_vecs.cpu()
            q_vecs = q_vecs.numpy()
        k = 10  # topk
        distance, topk = index.search(q_vecs, k)
        dataset = Q2Dataset(self.candidate_file)
        for i, q in enumerate(query):
            print('query: ', q)
            for j, idx in enumerate(topk[i]):
                print(f'{j}th nearest candidate: ', dataset[idx])


class FaissStreamSearcher:
    def __init__(self, num_gpu, local_rank, config):
        """
        先用模型对输入语句编码成向量，再用faiss进行向量检索。
        使用流式读写，用IncrementalPCA降维，增量构建faiss索引，适用于大规模数据。
        :param :
        """
        super().__init__()
        self.num_gpu = num_gpu
        self.batch_size = config['recall']['batch_size']
        self.max_seq_len = config['recall']['max_seq_len']
        # 候选文件
        self.candidate_file = config['inputs']['candidate_file']
        # PCA模型
        self.pca_dim = config['recall']['pca_dim']
        self.pca_checkpoint = config['recall']['pca_checkpoint']
        # 加载编码模型
        self.model = ErnieVectorizer()
        self.tokenizer = self.model.tokenizer
        # 在线编码地址 todo
        self.vectorizer_url = config['recall']['vectorizer_url']
        self.candidate_vecs = config['recall']['candidate_vecs']
        # put model to GPU if available
        self.local_rank = local_rank
        # torch.cuda.set_device(self.local_rank)
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def candidate_vectorize(self):
        """
        调用编码模型批量预测所有候选句子的特征向量，可分布式
        :return: 返回候选句子总数。向量保存为vec文件。
        """
        # 分布式训练，流式数据读取
        dataset = Q2StreamSubset(self.candidate_file, self.local_rank, self.num_gpu)
        with torch.no_grad():
            loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=False, pin_memory=True)
            if torch.cuda.is_available():
                # 平均每个文件接近10G
                file = f'candidates_part{self.local_rank}.vec'
            else:
                file = 'candidates.vec'

            with open(file, 'ab') as fw:
                for data in loader:
                    vec = infer_batch(data,
                                      self.model,
                                      self.tokenizer,
                                      self.max_seq_len)
                    if torch.cuda.is_available():
                        vec = vec.cpu()
                    pickle.dump(vec.numpy(), fw)

    def _interleave_sort(self, batches):
        """
        交错排序，恢复原始顺序，多个批次整合为一个批次
        :param batches: 若干批的 numpy array
        :return: 恢复顺序之后的统一批次的 numpy array
        """
        arr = []
        col = len(batches)
        for i in range(self.batch_size):
            for j in range(self.num_gpu):
                if j < col and i < batches[j].shape[0]:
                    arr.append(batches[j][i, :])
                else:
                    return np.stack(arr, axis=0).astype('float32')
        return np.stack(arr, axis=0).astype('float32')

    def batch_vec_gen(self):
        """
        单进程batch vector生成器
        从多个向量文件中轮流读取vector，按原始顺序拼成批vectors并流式生成。本身可以控制生成结束。
        批的数量：batch size * num gpu（最后一批除外）
        :return: yield 批vectors
        """
        if torch.cuda.is_available():
            file_handlers = []
            for i in range(self.num_gpu):
                # todo 配置
                file_handlers.append(open(f'/disk2/yangshansong/candidates_part{i}.vec', 'rb'))
            while True:
                batch_vecs = []
                try:
                    # 每个文件读取一个批，一轮共num gpu个批
                    for i in range(self.num_gpu):
                        # dump阶段序列化多个批对象，load阶段每次反序列化一个批对象
                        sub = pickle.load(file_handlers[i])
                        print('sub length: ', len(sub))
                        batch_vecs.append(sub)
                    print('batch_vecs length: ', len(batch_vecs))
                    # 生成器，批数据的数量是：batch_size * num_gpu
                    yield self._interleave_sort(batch_vecs)
                except EOFError:
                    # 流终止：最后一批可能不是每个文件都有，可能每个文件的shape不一样
                    if batch_vecs:
                        yield self._interleave_sort(batch_vecs)
                    break
        else:
            with open('candidates.vec', 'rb') as fr:
                while True:
                    try:
                        yield pickle.load(fr)
                    except EOFError:
                        break

    def pca_fit(self):
        """
        增量训练PCA模型，并保存
        Returns:
        """
        vec_gen = self.batch_vec_gen()
        pca = IncrementalPCA(n_components=self.pca_dim)
        # todo
        count = 1
        for batch_vec in tqdm(vec_gen):
            if count % 100 == 0:
                print('count: ', count)
            pca.partial_fit(batch_vec)
            count += 1
            if count == 1000:
                break
        with open(self.pca_checkpoint, 'wb') as fw:
            pickle.dump(pca, fw)
        print('PCA model trained and saved!')

    def pca_transform(self):
        """
        使用训练好的增量PCA模型对所有向量降维，并保存为一个npy文件
        Returns:
        """
        # 加载增量PCA模型
        with open(self.pca_checkpoint, 'rb') as fr:
            pca = pickle.load(fr)

        vec_gen = self.batch_vec_gen()
        vecs = []
        for batch_vec in tqdm(vec_gen):
            # PCA降维
            batch_vec = pca.transform(batch_vec)
            print('batch_vec: ', batch_vec)
            vecs.append(batch_vec)
            print('----------------')

        vecs = np.concatenate(vecs, axis=0).astype('float32')
        np.save('candidates_small.npy', vecs)
        print('vectors reduced and saved!')

    def build_ivf(self):
        """
        构建ivf索引，仅单进程。
        一次性加入向量，先用PCA模型降维，再加入索引。
        :return: 索引， pca模型
        """
        # 加载增量PCA模型
        with open(self.pca_checkpoint, 'rb') as fr:
            pca_model = pickle.load(fr)
            print("has loaded pca model")
        # 构建索引
        res = faiss.StandardGpuResources()  # use a single GPU
        measure = faiss.METRIC_L2
        param = 'IVF10000, PQ16'
        vec_index = faiss.index_factory(self.pca_dim, param, measure)
        if torch.cuda.is_available():
            vec_index = faiss.index_cpu_to_gpu(res, 0, vec_index)
        # 训练并加入向量
        vecs = np.load(self.candidate_vecs)
        vec_index.train(vecs)
        vec_index.add(vecs)
        print('index total rows: ', vec_index.ntotal)
        return vec_index, pca_model

    def build_hnsw(self):
        """
        构建hnsw索引，仅单进程。
        流式加入向量，先用PCA模型降维，再加入索引。
        :return: 索引，pca模型
        """
        # 加载增量PCA模型
        with open(self.pca_checkpoint, 'rb') as fr:
            pca_model = pickle.load(fr)
        # 构建索引
        res = faiss.StandardGpuResources()  # use a single GPU
        measure = faiss.METRIC_L2
        param = 'HNSW16'
        vec_index = faiss.index_factory(self.pca_dim, param, measure)
        if torch.cuda.is_available():
            vec_index = faiss.index_cpu_to_gpu(res, 0, vec_index)
        # 加入向量
        vecs = np.load(self.candidate_vecs)
        vec_index.add(vecs)
        print('index total rows: ', vec_index.ntotal)
        return vec_index, pca_model

    def recall(self, query, pca_model, index, k):
        """
        向量检索，Faiss语义索引
        :param query: 一批原始查询语句（不分词，仅q2）
        :param pca_model: 训练好的pca模型
        :param index: 索引
        :param k: 召回数量
        :return:
        """
        with torch.no_grad():
            t0 = time.time()
            # 查询向量化，通过ERNIE模型，获得查询的向量
            query_vecs = infer_batch(query, self.model, self.tokenizer, self.max_seq_len)
            if torch.cuda.is_available():
                query_vecs = query_vecs.cpu()
            query_vecs = query_vecs.numpy()
        t1 = time.time()
        # PCA降维
        query_vecs = pca_model.transform(query_vecs).astype('float32')
        t2 = time.time()
        # 语义检索
        distance, top = index.search(query_vecs, k)
        t3 = time.time()
        return distance, top, t1 - t0, t2 - t1, t3 - t2

    def recall_online(self, query, pca_model, index, k):
        """
        Faiss索引中检索，使用文本向量化服务
        :param query: 一个原始查询语句（不分词，仅q2）
        :param pca_model: 训练好的pca模型
        :param index: 索引
        :param k: 召回数量
        :return:
        """
        t0 = time.time()
        # 通过接口，获取查询向量化
        temp = requests.get(self.vectorizer_url + query)
        q_vecs = temp.json()
        q_vecs = np.reshape(q_vecs, (1, -1))
        t1 = time.time()
        q_vecs = pca_model.transform(q_vecs).astype('float32')
        t2 = time.time()
        distance, top = index.search(q_vecs, k)
        t3 = time.time()
        return distance, top, t1 - t0, t2 - t1, t3 - t2


def search_test():
    """
    基于向量化后的聊天数据库，通过Faiss，建立语义近邻索引，并搜索
    Returns:
    """
    indexer = FaissStreamSearcher(args, config_info)
    t0 = time.time()
    index, pca_model = indexer.build_hnsw()
    t1 = time.time()
    print(f'build index take {t1 - t0} seconds')
    qs = [
        '券商股疯了，大盘也是疯了，比疫情期间大跌还害怕。',
        '你好啊',
        '很高兴认识你',
        '我要去听相声了德云社的哦',
        '今年利物浦确实有冠军的实力'
    ]
    dist, tops, _, _, _ = indexer.recall(qs, pca_model, index, 1000)
    for dis in dist:
        row = pd.Series(dis)
        print(row.describe())


# python -m torch.distributed.launch --nproc_per_node=4 semantic_search.py
if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = '4,5,6,7'
    parser = argparse.ArgumentParser()
    # 注意local rank这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
    parser.add_argument("--local_rank", type=int)
    parser.add_argument("--num_gpu", type=int, default=4)
    args = parser.parse_args()
    local_rank = args.local_rank
    num_gpu = args.num_gpu

    config_file = "../config/config.json"
    with open(config_file, 'r') as f:
        config_info = json.load(f)

    # 如果gpu可用
    if torch.cuda.is_available():
        # 初始化分布式进程组
        torch.distributed.init_process_group(backend='NCCL', init_method='env://')
    # 令cuDNN可以使用非确定性算法
    cudnn.enabled = True
    # 令cuDNN的auto-tuner自动寻找最适合当前配置的高效算法
    cudnn.benchmark = True
    # 使用确定性算法
    cudnn.deterministic = True

    indexer = FaissStreamSearcher(local_rank, num_gpu, config_info)
    # indexer.candidate_vectorize()
    # indexer.pca_fit()
    # indexer.pca_transform()
    search_test()
