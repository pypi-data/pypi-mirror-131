# 正式线上服务
import torch
import numpy as np
import os
import json
import time
import argparse
from flask import Flask, request
app = Flask(__name__)

from recall.semantic_search import FaissStreamSearcher
from recall.es_search import ElasticObj
from rank.ranker import ErnieRanker
import onnxruntime
from model.ernie import convert_list_to_features


def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s


# 输入单个数据预测
@app.route('/onlineonnx', methods=['GET'])
def get_final():
    context = request.args.get('context')
    us = context.strip().split(sep)
    q2, kw_q2 = us[-1].split('|')[0], us[-1].split('|')[1:]
    # 召回
    _, topk, t_vec, t_pca, t_search = indexer.recall_online(q2, pca, index, k_index)
    topk = list(map(str, topk[0]))
    t0 = time.time()
    if not kw_q2:
        responses1, origins1 = es.recall(q2, topk, k_es)
    else:
        responses1, origins1 = es.recall(' '.join(kw_q2), topk, k_es)
    t01 = time.time()
    responses2, origins2 = es.recall_ids(topk[:20-len(responses1)])
    responses = responses1 + responses2
    origins = origins1 + origins2
    t1 = time.time()
    # rank
    if not responses:
        best, score = 'NA', 0
        t11 = t1
        t12 = t1
    else:
        query = '。'.join(us)
        input_ids, input_mask, segment_ids = convert_list_to_features(query, 30, matcher.tokenizer, responses)
        t11 = time.time()
        ort_inputs = {
            ort_session.get_inputs()[0].name: input_ids,
            ort_session.get_inputs()[1].name: input_mask,
            ort_session.get_inputs()[2].name: segment_ids
        }
        ort_outs = ort_session.run(None, ort_inputs)
        t12 = time.time()
        logits = sigmoid(ort_outs[0])
        score = float(np.max(logits))
        pred = np.argmax(logits)
        best = responses[pred]
    t2 = time.time()
    return json.dumps({'response': best,
                       'score': score,
                       'keywords': kw_q2,
                       'candidates': [o + sep + r for o, r in zip(origins, responses)],
                       'time': t2 - t0 + t_vec + t_pca + t_search,
                       't_vec': t_vec,
                       't_pca': t_pca,
                       't_search': t_search,
                       't_esid': t1 - t01,
                       't_esrecall': t01 - t0,
                       't_input': t11 - t1,
                       't_model': t12 - t11,
                       't_rank': t2-t1
                       })


# test the whole system
if __name__ == '__main__':
    config_file = "../config/config.json"
    with open(config_file, 'r') as f:
        config_info = json.load(f)
    k_index = config_info['recall']['index_topn']
    k_es = config_info['recall']['es_topn']
    sep = "||"

    os.environ["CUDA_VISIBLE_DEVICES"] = '3'

    parser = argparse.ArgumentParser()
    # 注意local rank这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
    parser.add_argument("--local_rank", type=int, default=0)
    parser.add_argument("--num_gpu", type=int, default=4)
    args = parser.parse_args()

    es = ElasticObj(config_info)

    matcher = ErnieRanker(config_info)

    so = onnxruntime.SessionOptions()
    so.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    ort_session = onnxruntime.InferenceSession("model/ernie_match.onnx", sess_options=so)
    ort_session.set_providers(['CUDAExecutionProvider'])

    indexer = FaissStreamSearcher(args, config_info)
    tt0 = time.time()
    index, pca = indexer.build_ivf()
    tt1 = time.time()
    print(f'build index take {tt1-tt0} seconds')

    app.run(host='0.0.0.0', port=6993, threaded=True)
