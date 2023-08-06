# @Time    : 2018/5/24 10:03
# @Author  : Niyoufa
import unittest
from microserver.cache.rediscache import RedisCache
from microserver.tests import print_testcase

class RedisTestCase(unittest.TestCase):

    @print_testcase
    def test_redis_connect(self):
        class TestRedisCache(RedisCache):
            pattern = ""
            alias_name = "redis_test"

            def get(self, key):
                return super(TestRedisCache, self).get(key)

        cache_obj = TestRedisCache()
        data = cache_obj.get("wechat_group_chat_aggregate")
        print(data)