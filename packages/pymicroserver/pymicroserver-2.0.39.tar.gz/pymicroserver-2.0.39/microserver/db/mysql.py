# @Time    : 2018/4/17 下午10:14
# @Author  : Niyoufa
import json
import pymysql
from datetime import datetime
from collections import namedtuple
from microserver.conf import settings
from microserver.db.base import BaseModel
from voluptuous import Schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, CHAR, TEXT, BigInteger, \
    String, DateTime, VARCHAR, Float, Boolean, BIGINT, UniqueConstraint, PrimaryKeyConstraint
from microserver.db.base import DBConfigExistError, ProjectError, SortError
Base = declarative_base()

DB_TEXT = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'

def get_engine(alias_name):
    mysql_config = settings.DATABASES.get(alias_name)
    host = mysql_config["host"]
    port = mysql_config["port"]
    user = mysql_config["user"]
    passwd = mysql_config["passwd"]
    database = mysql_config.get("database")
    engine = create_engine(DB_TEXT.format(user,
                                          passwd,
                                          host,
                                          port,
                                          database), echo=True)
    return engine

def get_session(alias_name):
    mysql_config = settings.DATABASES.get(alias_name)
    host = mysql_config["host"]
    port = mysql_config["port"]
    user = mysql_config["user"]
    passwd = mysql_config["passwd"]
    database = mysql_config.get("database")
    engine = create_engine(DB_TEXT.format(user,
                                          passwd,
                                          host,
                                          port,
                                          database))
    return sessionmaker(bind=engine)

def get_client(self, alias_name):
    mysql_config = settings.DATABASES.get(alias_name)
    host = mysql_config["host"]
    port = mysql_config["port"]
    user = mysql_config["user"]
    passwd = mysql_config["passwd"]
    database = self.database_name or mysql_config.get("database")
    charset = mysql_config.get("charset") or "utf8"
    client = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=database, charset=charset)
    return client


class BaseMySQL(BaseModel):
    _name = None
    _alias_name = "mysql"

    PRIMARY_KEY = "id"

    @property
    def query_where_statement(self):
        return 'where '

    @property
    def query_project(self):
        return {}

    def __init__(self, alias_name=None, name=None):
        if alias_name:
            self._alias_name = alias_name
        self._name = name or self._name
        args = self._name.split(".")
        self.database_name, self.table_name = args[0], args[1]

    def get_client(self):
        mysql_config = settings.DATABASES.get(self._alias_name)
        host = mysql_config["host"]
        port = mysql_config["port"]
        user = mysql_config["user"]
        passwd = mysql_config["passwd"]
        database = self.database_name or mysql_config.get("database")
        charset = mysql_config.get("charset") or "utf8"
        client = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=database, charset=charset)
        return client

    def get_engine(self, alias_name=None):
        mysql_config = settings.DATABASES.get(alias_name or self._alias_name)
        host = mysql_config["host"]
        port = mysql_config["port"]
        user = mysql_config["user"]
        passwd = mysql_config["passwd"]
        database = mysql_config.get("database")
        engine = create_engine(DB_TEXT.format(user,
                                              passwd,
                                              host,
                                              port,
                                              database), echo=True)
        return engine

    def get_session(self, alias_name=None):
        mysql_config = settings.DATABASES.get(alias_name or self._alias_name)
        host = mysql_config["host"]
        port = mysql_config["port"]
        user = mysql_config["user"]
        passwd = mysql_config["passwd"]
        database = mysql_config.get("database")
        engine = create_engine(DB_TEXT.format(user,
                                              passwd,
                                              host,
                                              port,
                                              database))
        return sessionmaker(bind=engine)

    def get_connection(self):
        engine = self.get_engine()
        connection = engine.connect()
        return connection

    def insert(self, vals, **kwargs):
        if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
            vals = self.scheme(vals)
        session = kwargs.get("session") or self.get_session()()
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        obj = self.__class__(**vals)
        session.add(obj)
        session.commit()
        insert_id = obj.id
        if session not in kwargs:
            session.close()
        return insert_id

    def update(self, id, vals, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        obj = session.query(self.__class__).filter(self.__class__.id==id).one()
        for k, v in vals.items():
            setattr(obj, k, v)
        session.commit()

        update_result = {}
        for column in obj.__table__.columns.keys():
            update_result.update({column: getattr(obj, column)})

        if session not in kwargs:
            session.close()
        return update_result

    def remove(self, id, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        obj = session.query(self.__class__).filter(self.__class__.id == id).one()
        session.delete(obj)
        session.commit()
        if session not in kwargs:
            session.close()

    def find_one(self, id, project=None, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        obj = session.query(self.__class__).filter(self.__class__.id == id).one()
        if session not in kwargs:
            session.close()
        find_one_result = {}
        for column in obj.__table__.columns.keys():
            find_one_result.update({column: getattr(obj, column)})
        if not find_one_result:
            return None
        return find_one_result

    def find_one_by_sql(self, sql, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        proxy = session.execute(sql)
        result = proxy.fetchone()
        if session not in kwargs:
            session.close()
        return result


    def find_one_by_query(self, query=None, project=None, **kwargs):
        session = kwargs.get("session") or self.get_session()()

        includes, _ = self.project_handle(project)
        if includes:
            Q = session.query(*tuple([getattr(self.__class__, column) for column in includes]))
        else:
            Q = session.query(self.__class__)

        filter_exp = kwargs.get("filter_exp")
        if filter_exp:
            Q = Q.filter(*tuple(filter_exp))

        if query:
            Q = Q.filter(*tuple([getattr(self.__class__, k) == v for k, v in query.items()]))

        obj = Q.first()
        if not obj:
            return obj

        if isinstance(obj, tuple):
            scheme = namedtuple("scheme", includes)
            obj = scheme(*obj)

        temp_obj = {}
        if includes:
            for field in includes:
                temp_obj.update({field: getattr(obj, field)})
        else:
            for field in obj.__table__.columns.keys():
                temp_obj.update({field: getattr(obj, field)})

        if session not in kwargs:
            session.close()
        return temp_obj

    def count(self, query=None, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        q = session.query(self.__class__)

        if query:
            sql_exp = []
            for k, v in query.items():
                sql_exp.append(getattr(self.__class__, k)==v)

            q = q.filter(*tuple(sql_exp))

        filter_exp = kwargs.get("filter_exp")
        if filter_exp:
            q = q.filter(*tuple(filter_exp))

        count = q.count()
        if session not in kwargs:
            session.close()
        return count

    def project_handle(self, project):
        includes = []
        excludes = []
        if project:
            if not isinstance(project, dict):
                raise ProjectError(project)

            project_items = project.items()
            for item in project_items:
                field = item[0]
                include = item[1]
                if include == 1:
                    includes.append(field)
                elif include == -1:
                    excludes.append(field)
                else:
                    raise ProjectError(project)

        return includes, excludes

    def search(self, query=None, sort=None, project=None, page=None, page_size=None, **kwargs):
        session = kwargs.get("session") or self.get_session()()

        includes, _ = self.project_handle(project)
        if includes:
            Q = session.query(*tuple([getattr(self.__class__, column) for column in includes]))
        else:
            Q = session.query(self.__class__)

        filter_exp = kwargs.get("filter_exp")
        if filter_exp:
            Q = Q.filter(*tuple(filter_exp))

        if query:
            Q = Q.filter(*tuple([getattr(self.__class__, k)==v for k, v in query.items()]))

        if sort:
            sort_items = sort.items()
            sort_list = []
            for item in sort_items:
                field = item[0]
                value = item[1]
                if value == 1 or value == "asc":
                    sort_list.append(getattr(self.__class__, field).asc())
                elif value == -1 or value == "desc":
                    sort_list.append(getattr(self.__class__, field).desc())
                else:
                    raise SortError(sort)
            Q = Q.order_by(*tuple(sort_list))

        if page != None:
            skip = self.page2skip(page, page_size)
        else:
            skip = 0

        if page_size != None:
            limit = int(page_size)
        else:
            limit = settings.PAGE_SIZE

        length = Q.count()
        pager = self.count_page(length, page, page_size=limit)

        Q = Q.offset(skip)
        Q = Q.limit(limit)

        search_result = Q.all()

        objs = []
        for obj in search_result:
            if isinstance(obj, tuple):
                scheme = namedtuple("scheme", includes)
                obj = scheme(*obj)

            temp_obj = {}
            if includes:
                for field in includes:
                    temp_obj.update({field: getattr(obj, field)})
            else:
                for field in obj.__table__.columns.keys():
                    temp_obj.update({field: getattr(obj, field)})
            objs.append(temp_obj)

        if session not in kwargs:
            session.close()
        return objs, pager

    def search_by_sql(self, sql, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        objs = session.execute(sql)
        return objs

    def bulk_create(self, body, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        for vals in body:
            key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
            vals["id"] = key
            obj = self.__class__(**vals)
            session.add(obj)
        session.commit()
        if session not in kwargs:
            session.close()

    def bulk_save(self, body, **kwargs):
        objects = []
        for vals in body:
            if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
                vals = self.scheme(vals)
            key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
            vals["id"] = key
            obj = self.__class__(**vals)
            objects.append(obj)
        if objects:
            session = kwargs.get("session") or self.get_session()()
            session.bulk_save_objects(objects, update_changed_only=False)
            session.commit()
            if session not in kwargs:
                session.close()

    def bulk_update(self, body):
        pass

    def bulk_delete(self, body, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        for vals in body:
            id = vals[self.PRIMARY_KEY]
            obj = session.query(self.__class__).filter(self.__class__.id == id).one()
            session.delete(obj)
        session.commit()
        if session not in kwargs:
            session.close()

    def bulk(self, body, **kwargs):
        pass

    def bulk_body_create(self, vals):
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        obj = self.__class__(**vals)
        return obj

    def bulk_body_index(self, vals):
        if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
            vals = self.scheme(vals)
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        obj = self.__class__(**vals)
        return obj

    def bulk_body_delete(self, id):
        vals = {}
        vals["id"] = id
        obj = self.__class__(**vals)
        return obj

    def bulk_body_update(self, id, vals):
        vals["id"] = id
        obj = self.__class__(**vals)
        return obj

    def get_max_id(self, **kwargs):
        session = kwargs.get("session") or self.get_session()()
        max_id = session.query(func.max(self.__class__.id)).one()[0] + 1
        if not "session" in kwargs:
            session.close()
        return max_id

class MySQL(BaseMySQL):
    id = Column(CHAR(length=255), primary_key=True)
    update_timestamp = Column(BIGINT, default=int(datetime.now().timestamp() * 1000), nullable=False)
    is_enable = Column(Boolean, default=True, nullable=False)