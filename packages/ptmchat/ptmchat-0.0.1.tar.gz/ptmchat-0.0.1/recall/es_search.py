# coding=utf-8
# WebURL：http://10.18.218.206:9100/
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time
import pandas as pd
import json


class ElasticObj:
    def __init__(self, config):
        # es settings
        self.index_type = config['es_info']['index_type']
        self.host = config['es_info']['es_host']
        self.user_name = config['es_info']['user_name']
        self.password = config['es_info']['password']
        self.es = Elasticsearch(hosts=[self.host], http_auth=(self.user_name, self.password), timeout=5000)
        self.index_alias = config['es_info']['index_alias']
        if self.es.indices.exists_alias(name=[self.index_alias]):
            self.old_index_name = list(self.es.indices.get_alias(name=[self.index_alias]).keys())[0]
        else:
            self.old_index_name = None
        self.index_name = config['es_info']['index_name_pre'] + time.strftime("%Y%m%d%H%M")

    def set_mapping(self):
        """
        设置映射，创建索引
        Returns:

        """
        body = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            },
            "mappings": {
                self.index_type: {
                    "properties": {
                        "query1": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_max_word"},
                        "response1": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_max_word"},
                        "query2": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_max_word"},
                        "response2": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_max_word"}
                    }
                }
            }
        }
        self.es.indices.create(index=self.index_name, ignore=True, body=body)

    def gen_file(self, file):
        """
        定义ES动作迭代器，数据插入
        从文件中流式生成每一条数据，并自带ID从0开始
        Args:
            file: tsv原始数据文件

        Returns:

        """
        # 流式读取CSV数据文件
        reader = pd.read_csv(file, sep='\t', header=0, na_filter=False, iterator=True, chunksize=1)
        count = -1  # 文件ID
        for chunk in reader:
            row = chunk.iloc[0]
            if row['visible'] == 0:
                continue
            count += 1
            # 定义数据文档
            document = {
                "query1": row['q1'],
                "response1": row['r1'],
                "query2": row['q2'],
                "response2": row['r2']
            }
            # 定义操作
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": count,
                "_source": document
            }
            yield action

    def write_data(self, source):
        """
        将数据写入索引
        Args:
            source:

        Returns:

        """
        # 创建数据操作迭代器
        gen = self.gen_file(source)
        t0 = time.time()
        success, _ = bulk(self.es, gen, index=self.index_name, raise_on_error=True)
        t1 = time.time()
        print(f'performed {success} actions in {(t1 - t0) / 60} minutes.')

    def shift_alias(self):
        """
        Shift the alias from old index to new index
        Returns:

        """
        if self.old_index_name is None:
            body = {
                "actions": [
                    {"add": {"index": self.index_name, "alias": self.index_alias}}
                ]
            }
            # 更新索引别名
            self.es.indices.update_aliases(body=body)
        else:
            body = {
                "actions": [
                    {"remove": {"index": self.old_index_name, "alias": self.index_alias}},
                    {"add": {"index": self.index_name, "alias": self.index_alias}}
                ]
            }
            # 更新索引别名
            self.es.indices.update_aliases(body=body)
            # 删除旧的索引
            self.es.indices.delete(index=self.old_index_name, ignore=[400, 404])

    def index_exist(self):
        """
        索引是否存在
        Returns:

        """
        return self.es.indices.exists(index=[self.index_name])

    @property
    def size(self):
        return self.es.count(index=self.index_name)

    def recall_ids(self, ids):
        """
        按id检索。
        :param ids: List[str] 文档的id列表
        :return: 所有文档
        """
        body = {
            "ids": ids
        }
        sources = ['query1', 'response1', 'query2', 'response2']
        # 索引查询是按照别名来指定具体索引
        hits = self.es.mget(body=body, index=self.index_alias, doc_type=self.index_type, _source=sources)
        all_sources = hits['docs']
        results = []
        contexts = []
        for hit in all_sources:
            if not hit['found']:
                raise KeyError(f"doc id {hit['_id']} not found in ES. Faiss and ES data may not be consistent!")
            result = hit['_source']['response2']
            results.append(result)
            context = hit['_source']['query1'] + '||' + hit['_source']['response1'] + '||' + hit['_source']['query2']
            contexts.append(context)
        return results, contexts

    def recall(self, query, ids, k):
        """
        按id和query检索。
        :param query: 一个query
        :param ids: List[str] 文档的id列表
        :param k: 召回几个
        :return: 所有文档
        """
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "query2": query
                            }
                        }
                    ],
                    "filter": [
                        {
                            "ids": {
                                "values": ids
                            }
                        }
                    ]
                }
            }
        }
        sources = ['query1', 'response1', 'query2', 'response2']
        # 索引查找，按照别名来指定具体索引
        hits = self.es.search(
            index=self.index_alias,
            body=body,
            _source=sources,
            size=k,
            track_total_hits=False,
            timeout="35ms")
        all_sources = hits['hits']['hits']
        results = []
        contexts = []
        count = len(all_sources)
        for i in range(count):
            source = all_sources[i]['_source']
            result = source['response2']
            results.append(result)
            context = source['query1'] + '||' + source['response1'] + '||' + source['query2']
            contexts.append(context)
        return results, contexts

    def recall_ext(self, keys, extends, ids, k):
        """
        按id和query关键词检索。扩展关键词。
        :param keys: query的关键词
        :param extends: 扩展的关键词 todo 扩展关键词，应该在context中出现
        :param ids: List[str] 文档的id列表
        :param k: 召回几个
        :return: 所有文档
        """
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "query2": ' '.join(keys + extends)
                            }
                        }
                    ],
                    "should": [
                        {
                            "multi_match": {
                                "query": ' '.join(keys),
                                "fields": ["query1", "response1", "query2^2"]
                            }
                        }
                    ],
                    "filter": [
                        {
                            "ids": {
                                "values": ids
                            }
                        }
                    ]
                }
            }
        }
        sources = ['query1', 'response1', 'query2', 'response2']
        hits = self.es.search(
            index=self.index_alias,
            body=body,
            _source=sources,
            size=k,
            track_total_hits=False,
            timeout="35ms")
        all_sources = hits['hits']['hits']
        results = []
        contexts = []
        count = len(all_sources)
        for i in range(count):
            source = all_sources[i]['_source']
            result = source['response2']
            results.append(result)
            context = source['query1'] + '||' + source['response1'] + '||' + source['query2']
            contexts.append(context)
        return results, contexts

    def test_analyzer(self, query, analyzer='ik_max_word'):
        """
        test the analyzer
        Args:
            query:
            analyzer:

        Returns:

        """
        body = {
            "analyzer": analyzer,
            "text": query
        }
        return self.es.indices.analyze(body=body, index='chat_all202106241410')

    def build_index(self, source):
        """
        构建索引
        Args:
            source:

        Returns:

        """
        # 设置映射，创建索引
        self.set_mapping()
        # 插入数据
        self.write_data(source)
        # 切换别名，删除旧索引
        self.shift_alias()


if __name__ == "__main__":
    with open('../config/config.json', 'r') as f:
        config_info = json.load(f)
    es = ElasticObj(config_info)
    # data = '../data/ernie_clean.tsv'
    # es.build_index(data)
    # res = es.recall_ids(['3205306', '8285888', '10720332', '12040142'])
    res = es.recall('会所那边的情况', ['3205306', '8285888', '10720332', '12040142'], 3)
    print(res)
    # print(es.test_analyzer("会所那边的情况", analyzer='ik_max_word'))
