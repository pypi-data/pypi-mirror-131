# @Time    : 2018/4/18 16:41
# @Author  : Niyoufa
import unittest
from microserver.tests import print_testcase
from elasticsearch import Elasticsearch
from microserver.db.es import ES
from microserver.db.base import AggregateBodyError


class ESTestCase(unittest.TestCase):

    def setUp(self):

        class TestModel(ES):
            _name = "law_case_info.case_info"
            _alias_name = "es_test"

        self.model = TestModel()

    def test_init(self):
        class Test1Model(ES):
            _name = None
            _alias_name = "es_test"

        class Test2Model(ES):
            _name = "law_case_info"
            _alias_name = "es_test"

        test1_model = Test1Model()
        test2_model = Test2Model()
        self.assertEqual(test1_model.index_name, None)
        self.assertEqual(test1_model.type_name, None)
        self.assertEqual(test2_model.index_name, "law_case_info")
        self.assertEqual(test2_model.type_name, None)

    @print_testcase
    def test_client(self):
        client = self.model.client
        self.assertIsInstance(client, Elasticsearch)

    @print_testcase
    def test_search(self):
        query = {"terms":{"id":["42b7318ce2c9ee9eeb14d3cfa2ea97ec", "42e57fe906433d82b2c49d9454b74fa0"]}}
        project = {"name":1, "provinceId":1}
        page = 1
        page_size = 2
        sort = {"provinceId":-1}
        objs, pager = self.model.search(
            query=query,
            project=project,
            page=page,
            page_size=page_size,
            sort = sort
        )

        if objs:
            includes = [item[0] for item in project.items() if item[1] == 1]
            self.assertEqual(len(includes), len(objs[0].keys()))
            for field in includes:
                self.assertIn(field, objs[0].keys())

        self.assertEqual(len(objs), page_size)

        provinceIds = [obj.get("provinceId") for obj in objs]
        self.assertEqual(sorted(provinceIds, reverse=True), provinceIds)

    def test_sort_asc(self):
        sort = {"provinceId": 1}
        objs, pager = self.model.search(
            sort=sort
        )

        provinceIds = [obj.get("provinceId") for obj in objs]
        self.assertEqual(sorted(provinceIds), provinceIds)

    def test_elasticsearch_aggregate(self):
        with self.assertRaises(AggregateBodyError):
            self.model.elasticsearch_aggregate({})

        body = {
            "province_agg": {
              "terms": {
                "field": "provinceId",
                "size": 1000
              }
            }
        }
        aggs_result = self.model.elasticsearch_aggregate(body=body)
        self.assertIn("aggregations", aggs_result.keys())

    def test_elasticsearch_bulk(self):
        id = "42bf8d95ee4ca36109308959cda25349"
        doc = {"provinceId": 2}
        body = self.model.bulk_body_update(id, doc)
        self.model.elasticsearch_bulk(body)

        project = {"provinceId":1}
        obj = self.model.find_one(id, project=project)
        for k, v in obj.items():
            self.assertEqual(v, doc[k])

    def test_search_read(self):
        query_params = self.model.bool_filter_query
        project = {"name": 1, "provinceId": 1}
        page = 1
        page_size = 2
        sort_params = {"provinceId": -1}
        objs, pager = self.model.search_read(
            page, page_size,
            query_params=query_params,
            _project=project,
            sort_params=sort_params
        )

        if objs:
            includes = [item[0] for item in project.items() if item[1] == 1]
            self.assertEqual(len(includes), len(objs[0].keys()))
            for field in includes:
                self.assertIn(field, objs[0].keys())

        self.assertEqual(len(objs), page_size)

        provinceIds = [obj.get("provinceId") for obj in objs]
        self.assertEqual(sorted(provinceIds, reverse=True), provinceIds)

    def test_mget(self):
        id = "32f7a5c959f8643a3c806353dc752a3a"
        objs = self.model.mget([id], _source_include=["id"])

