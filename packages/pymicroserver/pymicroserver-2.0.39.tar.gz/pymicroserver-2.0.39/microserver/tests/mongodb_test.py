# @Time    : 2018/4/23 15:48
# @Author  : Niyoufa
import unittest
from microserver.tests import print_testcase
from voluptuous import Schema, Required
from voluptuous.error import MultipleInvalid
import pymongo
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from microserver.db.mongodb import MongoDB


class MongoDBTestCase(unittest.TestCase):

    def setUp(self):
        class TestModel(MongoDB):
            _name = "test.test"
            _alias_name = "mongodb_test"

        self.model = TestModel()

    @print_testcase
    def test_init(self):
        self.assertIsInstance(self.model.client, pymongo.MongoClient)
        self.assertIsInstance(self.model.coll, Collection)

    @print_testcase
    def test_search(self):
        objs, pager = self.model.search()
        self.assertEqual(type(objs), list)
        self.assertEqual(type(pager), dict)

        pager_scheme = Schema({
            Required("page_size"): int,
            Required("max_page"): int,
            Required("pages"): list,
            Required("page_num"): int,
            Required("skip"): int,
            Required("page"): int,
            Required("enable"): bool,
            Required("has_more"): bool,
            Required("total"): int,
        }, extra=False)
        self.assertEqual(pager_scheme(pager), pager)

        query = {"name":"test"}
        objs, _ = self.model.search(query)
        for obj in objs:
            self.assertEqual(obj["name"], "test")

    @print_testcase
    def test_insert_and_find_one(self):
        id = self.model.insert({"name":"test"})
        with self.assertRaises(DuplicateKeyError):
            vals = {"id":id, "name":"test"}
            self.model.insert(vals)

        obj = self.model.find_one(id)
        scheme = Schema({
            Required("id"): str,
            Required("name"): str
        }, extra=False)
        self.assertEqual(scheme(obj), obj)

        with self.assertRaises(MultipleInvalid):
            obj = self.model.find_one(id, {"id":-1})
            scheme(obj)

        self.assertEqual(obj["name"], "test")

    @print_testcase
    def test_remove(self):
        id = self.model.insert({"name": "test"})
        self.model.remove(id)
        count = self.model.count({"id": id})
        self.assertEqual(count, 0)

    @print_testcase
    def test_update(self):
        id = self.model.insert({"name": "test"})
        self.model.update(id, {"name": "test1"})
        obj = self.model.find_one(id)
        self.assertEqual(obj["name"], "test1")

    def test_aggregate(self):
        pass

    def test_bulk(self):
        pass

    def test_update_by_query(self):
        pass

    def test_remove_by_query(self):
        pass

    def test_count(self):
        pass