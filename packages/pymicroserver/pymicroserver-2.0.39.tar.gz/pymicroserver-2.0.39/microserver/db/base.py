# @Time    : 2018/4/7 下午5:57
# @Author  : Niyoufa
import math
from abc import ABCMeta, abstractmethod
from bson import ObjectId
from microserver.core.exceptions import HandlerError, ArgumentTypeError
from microserver.utils.collections import BaseEnum


class QueryMode(BaseEnum):
    MONGODB = (1, "mongodb")
    ELASTICSEARCH = (10, "elasticsearch")
    MYSQL = (20, "mysql")
    DOMAIN = (30, "odoo domain")


class DBConfigExistError(HandlerError):
    def __init__(self, arg_name):
        super(DBConfigExistError, self).__init__(
            500, "数据库配置不存在 '%s'" % arg_name)
        self.arg_name = arg_name
        self.reason = "数据库配置不存在 '%s'" % arg_name


class ProjectError(HandlerError):
    def __init__(self, arg_name):
        super(ProjectError, self).__init__(
            500, "查询指定返回字段参数错误 '%s'" % arg_name)
        self.arg_name = arg_name
        self.reason = "查询指定返回字段参数错误 '%s'" % arg_name


class QueryModeError(HandlerError):
    """暂不支持查询模式异常"""

    def __init__(self, arg_name):
        super(QueryModeError, self).__init__(
            500, '暂不支持查询模式 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '暂不支持查询模式 %s' % arg_name


class SortError(HandlerError):
    """暂不支持查询模式异常"""

    def __init__(self, arg_name):
        super(SortError, self).__init__(
            500, '排序参数错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '排序参数错误 %s' % arg_name


class AggregateBodyError(HandlerError):
    """聚合参数错误"""

    def __init__(self, arg_name):
        super(AggregateBodyError, self).__init__(
            500, '聚合参数错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '聚合参数错误 %s' % arg_name


class IndexCreateError(HandlerError):
    """索引创建错误"""

    def __init__(self, arg_name):
        super(IndexCreateError, self).__init__(
            500, '索引创建错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '索引创建错误 %s' % arg_name


class FindOneIdError(HandlerError):
    """获取单条数据id参数错误"""

    def __init__(self, arg_name):
        super(FindOneIdError, self).__init__(
            500, '获取单条数据id参数错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '获取单条数据id参数错误 %s' % arg_name


class HasExistError(HandlerError):
    """已存在"""

    def __init__(self, arg_name):
        super(HasExistError, self).__init__(
            500, '已存在：%s'% arg_name
        )
        self.arg_name = arg_name
        self.reason = '已存在：%s'% arg_name


class BaseModel(object):
    ArgumentTypeError = ArgumentTypeError

    def search(
            self,
            query=None,
            sort=None,
            project=None,
            page=None,
            page_size=None):
        """
        查询符合条件的记录
        :param args:
        :param offset:
        :param limit:
        :param order:
        :param count:
        :return:
        """
        raise NotImplementedError()

    def aggregate(self, body, **kwargs):
        """
        聚合
        :param body:
            project：修改输入文档的结构。
            match：用于过滤数据，只输出符合条件的文档。
            limit：用来限制返回的文档数。
            skip：在聚合管道中跳过指定数量的文档，并返回余下的文档。
            sort：将输入文档排序后输出。
            group：将集合中的文档分组，可用于统计结果。
                $sum	计算总和。
                $avg	计算平均值。
                $min	获取集合中所有文档对应值得最小值。
                $max	获取集合中所有文档对应值得最大值。
                $push	在结果文档中插入值到一个数组中。
                $addToSet	在结果文档中插入值到一个数组中，但不创建副本。
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def bulk(self, body, **kwargs):
        """
        批量操作
        :param body:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def find_one(self, id, project=None, **kwargs):
        """
        获取一条记录
        :param id:
        :return:
        """
        raise NotImplementedError()

    def find_one_by_query(self, query, project=None, **kwargs):
        """
        根据查询条件获取一条记录
        :param query: 
        :param project: 
        :param kwargs: 
        :return: 
        """
        raise NotImplementedError()

    def insert(self, vals, **kwargs):
        """
        插入一条记录
        :param vals: 待插入记录的字段和值，字典类型
        :return:新建记录的id
        """
        raise NotImplementedError()

    def update(self, id, vals, **kwargs):
        """
        更新一条或几条记录
        :param vals: 待新建记录的字段和值，字典类型
        :param kwargs:
        upsert:
        :return:新建记录的id
        """
        raise NotImplementedError()

    def update_by_query(self, query, vals, **kwargs):
        """
        根据查询条件更新
        :param query:
        :param vals:
        :param kwargs:
        :return:
        """

    def remove(self, id, **kwargs):
        """
        删除一条或几条记录
        :param query:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def remove_by_query(self, query, **kwargs):
        """
        根据查询条件删除
        :param query:
        :param kwargs:
        :return:
        """

    # 获取数量
    def count(self, query):
        """
        获取数量
        :param query_params:
        :return:
        """
        raise NotImplementedError()

    def skip2page(self, skip, limit):
        skip = int(skip)
        limit = int(limit)
        if skip < limit:
            page = 1
        else:
            page = int(skip // limit)
        return page

    def page2skip(self, page, page_size):
        page = int(page)
        page_size = int(page_size)
        if page < 1:
            skip = 0
        else:
            skip = (page - 1) * page_size
        return skip

    # 计算分页信息
    def count_page(
            self,
            length,
            page,
            page_size=10,
            page_show=10):
        if page:
            page = int(page)
        else:
            page = 1

        if page_size:
            page_size = int(page_size)
        else:
            page_size = 1

        length = int(length)
        if length == 0:
            return {"enable": False,
                    "page_size": page_size,
                    "skip": 0}
        max_page = int(math.ceil(float(length) / page_size))
        page_num = int(math.ceil(float(page) / page_show))
        pages = list(range(1, max_page + 1)
                     [((page_num - 1) * page_show):(page_num * page_show)])
        skip = (page - 1) * page_size
        if page >= max_page:
            has_more = False
        else:
            has_more = True
        pager = {
            "page_size": page_size,
            "max_page": max_page,
            "pages": pages,
            "page_num": page_num,
            "skip": skip,
            "page": page,
            "enable": True,
            "has_more": has_more,
            "total": length,
        }
        return pager

    def gen_objectid(self, oid=None):
        if oid:
            ObjectId(oid)
            object_id = oid
        else:
            object_id = str(ObjectId())
        return object_id

    @classmethod
    def gen_objectid(self, oid=None):
        if oid:
            ObjectId(oid)
            object_id = oid
        else:
            object_id = str(ObjectId())
        return object_id


class Cache(metaclass=ABCMeta):
    pattern = ""

    @abstractmethod
    def init_cache(self):
        """
        初始化缓存
        :return:
        """

    @abstractmethod
    def get(self, key):
        """
        获取值
        :param key:
        :return:
        """

    @abstractmethod
    def set(self, key, value):
        """
        设置值
        :param key:
        :param value:
        :return:
        """
