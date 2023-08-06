"""
独立的多轮聊天服务
"""
import tornado.httpserver
import tornado.ioloop
from tornado.options import define
import tornado.web
import os
import json
import time
import argparse
import random
import requests
from collections import defaultdict
import sys

sys.path.append("/tmp/pycharm_project_201/ptmchat_develop/")
from recall.semantic_search import FaissStreamSearcher
from recall.es_search import ElasticObj
from rank.ranker import ErnieRanker

keywords_url = 'http://10.18.217.184:8077/queryprocv2?userId=yuewenhao&type=TV&query='


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


# 兜底语句
def getfile(file):
    with open(file, 'r', encoding="utf8") as fr:
        data = fr.readlines()
    return map(lambda x: ''.join(x.strip().split()[1:]), data)


class ChatService:
    def __init__(self, config_info, args):
        self.doudi_response = list(getfile(config_info['inputs']['doudi_response_file']))
        self.es = ElasticObj(config_info)
        self.k_index = config_info['recall']['index_topn']
        self.k_es = config_info['recall']['es_topn']
        self.max_seq_num = 16

        self.matcher = ErnieRanker(config_info)
        self.matcher.load_model()

        self.indexer = FaissStreamSearcher(args, config_info)
        t0 = time.time()
        self.index, self.pca = self.indexer.build_ivf()
        t1 = time.time()
        print(f'build index take {t1 - t0} seconds')

    def chat(self, userID, q2):
        """
        :param userID: 用户id或设备id，用于区分不同用户的聊天历史
        :param q2: 用户当前query str type
        :return:
        """
        global history
        # if userID not in history:
        #     raise KeyError('userID not registered yet!')
        if len(history[userID]) > 1 and history[userID][-2][0] == "再见":
            # 清掉之前的对话历史
            history[userID] = []

        if len(history[userID]) > self.max_seq_num:
            # 顶掉较早的历史
            history[userID].pop(0)
            history[userID].pop(0)

        if len(history[userID]) >= 2:  # 判断是否是第一轮
            q1, r1 = history[userID][-2][0], history[userID][-1]
        else:
            q1, r1 = "nan", "nan"
        kw_q2 = get_keywords(q2)
        # 召回
        _, topk, t_vec, t_pca, t_search = self.indexer.recall([q2], self.pca, self.index, self.k_index)
        topk = list(map(str, topk[0]))
        if not kw_q2:
            responses1, origins1 = self.es.recall(q2, topk, self.k_es)
        else:
            responses1, origins1 = self.es.recall(' '.join(kw_q2), topk, self.k_es)
        responses2, origins2 = self.es.recall_ids(topk[:10])
        responses = responses1 + responses2
        origins = origins1 + origins2
        # rank
        if not responses:
            score = 0
            best = random.choice(self.doudi_response)
        else:
            contexts = ['。'.join([q1, r1, q2])] * len(responses)
            best, score = self.matcher.predict(contexts, responses)
        # 本轮写入历史
        candidates = [o + '||' + r for o, r in zip(origins, responses)]
        history[userID].append((q2, candidates, kw_q2, score))
        history[userID].append(best)
        return history[userID]


class ResultHandler(tornado.web.RequestHandler):
    def get(self):
        last_query = self.get_argument('query')
        userID = self.get_argument("userID")
        history[userID] = chatter.chat(userID, last_query)
        result = {"userID": userID}
        for i in range(len(history[userID])):
            if i % 2:
                # bot
                key = f"chatbot_turn_{i // 2 + 1}"
                result[key] = history[userID][i]
            else:
                # user
                key = f"user_turn_{i // 2 + 1}"
                result[key] = history[userID][i][0]
                if userID == 'test' and i == len(history[userID]) - 2:
                    # 测试账号，显示更多细节
                    result[f"score_turn_{i // 2 + 1}"] = history[userID][i][3]
                    result[f"topn_turn_{i // 2 + 1}"] = history[userID][i][1]
                    result[f"keywords_turn_{i // 2 + 1}"] = history[userID][i][2]
        self.write(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    # 导入配置文件
    config_file = "../config/config.json"
    with open(config_file, 'r') as f:
        config_info = json.load(f)

    os.environ["CUDA_VISIBLE_DEVICES"] = '3'

    parser = argparse.ArgumentParser()
    # 注意local rank这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
    parser.add_argument("--local_rank", type=int, default=0)
    parser.add_argument("--num_gpu", type=int, default=4)
    args = parser.parse_args()

    # history的key为用户id或设备id，自定义
    history = defaultdict(list)
    chatter = ChatService(config_info, args)

    # web service
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/subj_extract', ResultHandler),
        ],  # 网页路径控制
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(6996)
    tornado.ioloop.IOLoop.instance().start()
