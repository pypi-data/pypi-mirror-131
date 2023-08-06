# 测试线上服务
import os
import json
import time
import argparse
import requests
from flask import Flask, request
app = Flask(__name__)

import turbo_transformers
import torch
from model.turbo_match import ErnieMatchTurbo
from recall.semantic_search import FaissStreamSearcher
from recall.es_search import ElasticObj
from model.ernie import convert_list_to_features, new_tensor


keywords_url = 'http://10.18.217.184:8077/queryprocv2?userId=yuewenhao&type=TV&query='
# 从主服务获取tag和keyword labeling作为关键词
def get_keywords(sentence):
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


# 输入单个数据预测
@app.route('/chat', methods=['GET'])
def get_final():
    context = request.args.get('context')
    us = context.strip().split(sep)
    kw_q2 = get_keywords(us[-1])
    # 召回
    _, topk, t_vec, t_pca, t_search = indexer.recall(us[-1:], pca, index, k_index)
    topk = list(map(str, topk[0]))
    t0 = time.time()
    if not kw_q2:
        responses1, origins1 = es.recall(us[-1], topk, k_es)
    else:
        responses1, origins1 = es.recall(' '.join(kw_q2), topk, k_es)
    t01 = time.time()
    responses2, origins2 = es.recall_ids(topk[:10])
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
        input_ids, input_mask, segment_ids = convert_list_to_features(query, 30, turbo_model.tokenizer, responses)
        t11 = time.time()
        input_ids = new_tensor(input_ids)
        input_mask = new_tensor(input_mask)
        segment_ids = new_tensor(segment_ids)
        logits = turbo_model(input_ids, input_mask, segment_ids)
        logits = torch.sigmoid(logits)
        score = torch.max(logits).item()
        pred = torch.argmax(logits).item()
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
                       't_model': t2 - t11,
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

    os.environ["CUDA_VISIBLE_DEVICES"] = '7'

    parser = argparse.ArgumentParser()
    # 注意local rank这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
    parser.add_argument("--local_rank", type=int, default=0)
    parser.add_argument("--num_gpu", type=int, default=4)
    args = parser.parse_args()

    es = ElasticObj(config_info)

    turbo_transformers.set_num_threads(4)
    turbo_model = ErnieMatchTurbo(config_info)

    indexer = FaissStreamSearcher(args, config_info)
    tt0 = time.time()
    index, pca = indexer.build_ivf()
    tt1 = time.time()
    print(f'build index take {tt1-tt0} seconds')

    app.run(host='0.0.0.0', port=6996, threaded=True)
