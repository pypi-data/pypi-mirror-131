# @Time    : 2018/4/19 17:01
# @Author  : Niyoufa
from redis import ConnectionPool, Redis
from microserver.db.base import Cache, DBConfigExistError
from microserver.conf import settings


class RedisCache(Cache):
    alias_name = None
    pattern = ""

    def __init__(self):
        self.get_client()

    def get_client(self):
        config = settings.DATABASES.get(self.alias_name)
        if not config:
            raise DBConfigExistError("{klass}, alias_name:{alias_name}".format(
                klass=self.__class__.__name__,
                alias_name=self.alias_name,
            ))

        max_connection = config.get("redis_max_connection")

        connection_kwargs = dict()
        host = config.get("host")
        port = config.get("port")
        db = config.get("db")
        password = config.get("password")
        connection_kwargs.update(dict(
            host = host,
            port = port,
            db = db,
            password = password
        ))
        self.__connection_pool = ConnectionPool(max_connections=max_connection, **connection_kwargs)
        self.__redis = self.get_redis()
        return self

    ##############
    ### 字典数据操作
    ##############

    def init_cache(self):
        pass

    def set(self, key,value, **kwargs):
        key = "".join([self.pattern, key])
        self.__redis.set(key,value, **kwargs)

    def get(self, key):
        key = "".join([self.pattern, key])
        value = self.__redis.get(key)
        try:
            value = value.decode()
        except:
            pass
        return value

    # 保存一条记录，默认添加到最前面
    def save_key_value(self, key, value, append=False):
        key = "".join([self.pattern, key])
        if append:
            self.__redis.rpush(key, value)
        else:
            self.__redis.lpush(key, value)

    # 保存多条记录，默认添加到最前面
    def save_key_values(self, key, value_list, append=False):
        key = "".join([self.pattern, key])
        if not isinstance(value_list, list) and not isinstance(value_list, tuple):
            return
        if len(value_list) <= 0:
            return
        if append:
            self.__redis.rpush(key, *value_list)
        else:
            self.__redis.lpush(key, *value_list)

    # 获取一条记录
    def get_key_value(self, key, index):
        key = "".join([self.pattern, key])
        value = self.__redis.lindex(key, index)
        return value

    # 获取多条记录
    def get_key_values(self, key, start=0, end=-1):
        key = "".join([self.pattern, key])
        values = self.__redis.lrange(key, start, end)
        return values

    # 获取键对应记录集的长度
    def get_key_values_length(self, key):
        key = "".join([self.pattern, key])
        length = self.__redis.llen(key)
        return length

    # 删除一条记录
    def delete_key_value(self, key, value):
        key = "".join([self.pattern, key])
        self.__redis.lrem(key, value)

    # 删除多条记录
    def delete_key_values(self, key, value_list):
        key = "".join([self.pattern, key])
        for value in value_list:
            self.__redis.lrem(key, value)

    # 删除一个key
    def delet_key(self, key):
        key = "".join([self.pattern, key])
        self.__redis.delete(key)

    # key是否存在
    def has_key(self, key):
        key = "".join([self.pattern, key])
        return self.__redis.exists(key)

    # 创建一个key,并添加值(如果key存在，则先删除再创建)
    def create_key_values(self, key, value_list, append=False):
        key = "".join([self.pattern, key])
        if self.has_key(key):
            self.delet_key(key)
        self.save_key_values(key, value_list, append)

    # 获得一个redis实例
    def get_redis(self):
        return Redis(connection_pool=self.__connection_pool)

    #创建一个key-value
    def set_redis_key_value(self, key, value):
        key = "".join([self.pattern, key])
        self.__redis.set(key,value)

    # 获取keys
    def get_keys(self, pattern):
        cache_keys = self.__redis.keys(pattern)
        keys = [key.decode("utf-8") for key in cache_keys]
        return keys

    ##############
    ### 集合数据操作
    ##############

    # 向集合中添加一个或多个成员
    def sadd(self, key, *members):
        key = "".join([self.pattern, key])
        self.__redis.sadd(key, *members)

    # 获取集合的成员数
    def scard(self, key):
        key = "".join([self.pattern, key])
        return self.__redis.scard(key)

    # 判断 member 元素是否是集合 key 的成员
    def sismember(self, key, member):
        key = "".join([self.pattern, key])
        return self.__redis.sismember(key, member)

    # 返回集合中的所有成员
    def smembers(self, key):
        key = "".join([self.pattern, key])
        return self.__redis.smembers(key)

    # 将 member 元素从 source 集合移动到 destination 集合
    def smove(self, source, destination, member):
        self.__redis.smove(source, destination, member)

    # 返回集合中一个或多个随机数
    def srandmember(self, key, count=1):
        key = "".join([self.pattern, key])
        return self.__redis.srandmember(key, count)

    # 移除集合中一个或多个成员
    def srem(self, key, *members):
        key = "".join([self.pattern, key])
        self.__redis.srem(key, *members)