# 测试线上服务
import os
import json
import time
import argparse
import requests
from flask import Flask, request
import sys

app = Flask(__name__)
sys.path.append("/tmp/pycharm_project_201/ptmchat_develop/")
from recall.semantic_search import FaissStreamSearcher
from recall.es_search import ElasticObj
from rank.ranker import ErnieRanker

es = None
sep = "||"
index = None
pca = None
k_index = None
k_es = None
indexer = None
matcher = None

keywords_url = 'http://10.18.217.184:8077/queryprocv2?userId=yuewenhao&type=TV&query='


def get_keywords(sentence):
    """
    获取语句的关键词，依赖于语义主服务
    Args:
        sentence:

    Returns:

    """
    kw = []
    try:
        temp = requests.get(keywords_url + sentence)
        body = temp.json()
        tag_result = body['SemanticResult']['tagResults']
        for tw in tag_result:
            kw.append(tw['word'])
        labeling = body['KeywordLabeling']['keyword']
        kw.extend(labeling)
        kw = list(set(kw))
    except:
        return []
    return kw


@app.route('/chat', methods=['GET'])
def get_final():
    """
    获取聊天回复
    Returns:

    """
    context = request.args.get('context')
    us = context.strip().split(sep)
    # 获取查询关键词
    kw_q2 = get_keywords(us[-1])
    print("query: ", us[-1])
    print("keywords: ", kw_q2)
    # 语义近似召回
    _, topk, t_vec, t_pca, t_search = indexer.recall(us[-1:], pca, index, k_index)
    topk = list(map(str, topk[0]))
    t0 = time.time()
    # 文本近似召回
    if not kw_q2:
        responses1, origins1 = es.recall(us[-1], topk, k_es)
    else:
        responses1, origins1 = es.recall(' '.join(kw_q2), topk, k_es)
    t01 = time.time()
    responses2, origins2 = es.recall_ids(topk[:10])
    responses = responses1 + responses2
    origins = origins1 + origins2
    t1 = time.time()
    if not responses:
        best, score = 'NA', 0
    else:
        contexts = ['。'.join(us)] * len(responses)
        # 语义匹配排序
        best, score = matcher.predict(contexts, responses)
        print(best)
    t2 = time.time()
    result = json.dumps({'response': best,
                         'score': score,
                         'keywords': kw_q2,
                         'candidates': [o + sep + r for o, r in zip(origins, responses)],
                         'time': t2 - t0 + t_vec + t_pca + t_search,
                         't_vec': t_vec,
                         't_pca': t_pca,
                         't_search': t_search,
                         't_esid': t1 - t01,
                         't_esrecall': t01 - t0,
                         't_input': 0,
                         't_model': 0,
                         't_rank': t2 - t1
                         }, ensure_ascii=False)
    print(result)
    return result


def deploy(config_info):
    global es, sep, index, pca, k_index, k_es, indexer, matcher
    k_index = config_info['recall']['index_topn']
    k_es = config_info['recall']['es_topn']
    sep = "||"

    os.environ["CUDA_VISIBLE_DEVICES"] = '3,4,5,6'

    # parser = argparse.ArgumentParser()
    # 注意local rank这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
    # parser.add_argument("--local_rank", type=int, default=0)
    # parser.add_argument("--num_gpu", type=int, default=4)
    # args = parser.parse_args()
    local_rank = 4
    num_gpu = 4

    es = ElasticObj(config_info)

    matcher = ErnieRanker(config_info)
    matcher.load_model()

    indexer = FaissStreamSearcher(local_rank, num_gpu, config_info)
    tt0 = time.time()
    index, pca = indexer.build_ivf()
    tt1 = time.time()
    print(f'build index take {tt1 - tt0} seconds')

    app.run(host='0.0.0.0', port=6997, threaded=True)


# 聊天服务部署
if __name__ == '__main__':
    config_file = "../config/config.json"
    with open(config_file, 'r') as f:
        config_info = json.load(f)
    deploy(config_info)
