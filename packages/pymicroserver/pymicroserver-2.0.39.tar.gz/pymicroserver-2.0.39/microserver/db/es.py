# @Time    : 2018/4/17 下午10:07
# @Author  : Niyoufa
import certifi
import elasticsearch as es
from voluptuous import Schema
from bson.objectid import ObjectId
from microserver.conf import settings
from microserver.utils.decorator import time_consume
from microserver.db.base import BaseModel, QueryMode
from microserver.db.base import DBConfigExistError, ProjectError, \
    QueryModeError, SortError, AggregateBodyError, IndexCreateError


class ES(BaseModel):
    _name = None
    _alias_name = None

    PRIMARY_KEY = "id"

    index_mapping_body = None

    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "analysis": {
                "filter": {
                    "my_stopwords": {
                        "type": "stop",
                        "stopwords_path": "stopwords.txt"
                    }
                },
                "tokenizer": {
                    "my_pinyin": {
                        "type": "pinyin",
                        "keep_separate_first_letter": False,
                        "keep_full_pinyin": True,
                        "keep_original": True,
                        "limit_first_letter_length": 16,
                        "lowercase": True,
                        "remove_duplicated_term": True
                    }
                },
                "analyzer": {
                    "max_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_max_word",
                        "char_filter": [
                            "html_strip"
                        ]
                    },
                    "smart_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_smart",
                        "char_filter": [
                            "html_strip"
                        ]
                    },
                    "pinyin_analyzer": {
                        "type": "custom",
                        "tokenizer": "my_pinyin"
                    }
                }
            }
        }
    }

    default_mapping_properties = {
        "id": {
            "type": "keyword"
        },
        "update_time": {
            "type": "long",
        },
        "is_enable": {
            "type": "boolean",
        },
    }

    query_template = {

        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "bool": {
                        "must": [],
                        "must_not": [],
                        "should": []
                    }
                }
            }
        },

        "size": 10,

        "from": 0,

        "sort": [
            {
                "_id": {
                    "order": "desc"
                }
            }
        ],

        "_source": [
            "name",
            "id"
        ],

        "aggs": {
            "province_agg": {
                "terms": {
                    "field": "provinceId",
                    "size": 1000
                }
            }
        },

        "highlight": {
            "pre_tags": [
                "<em>"
            ],
            "post_tags": [
                "</em>"
            ],
            "fields": {
                "body": {
                    "number_of_fragments": 1,
                    "fragment_size": 20
                },
            }
        },
    }
    default_query = query_template["query"]
    default_sort = query_template["sort"]
    default_source = query_template["_source"]
    default_from = query_template["from"]
    default_size = query_template["size"]

    match_all_query = {
        "match_all": {}
    }

    match_query = {
        "match": {}
    }

    multi_match_query = {
        "multi_match": {
            "query": "",
            "fields": []
        }
    }

    bool_query = {
        "bool": {
            "must": [],
            "must_not": [],
            "should": []
        }
    }

    wildcards_query = {
        "wildcard": {}
    }

    regex_query = {
        "regex": {}
    }

    prefix_query = {
        "prefix": {}
    }

    match_phrase_query = {
        "match_phrase": {}
    }

    term_filter = {
        "term": {}
    }

    terms_filter = {
        "terms": []
    }

    range_filter = {
        "range": {}
    }

    exists_filter = {
        "exists": {}
    }

    bool_filter = {
        "must": [],
        "must_not": [],
        "should": []
    }

    bool_filter_query = {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "bool": {"must": []}
                }
            }
        }
    }

    def __init__(self, alias_name=None, name=None):
        if alias_name:
            self._alias_name = alias_name
        self._name = name or self._name
        try:
            self.index_name = self._name.split(".")[0]
        except:
            self.index_name = None
        try:
            self.type_name = self._name.split(".")[1]
        except:
            self.type_name = None
        self.client = self.get_client()

    def get_client(self):
        es_config = settings.DATABASES.get(self._alias_name)
        if not es_config:
            raise DBConfigExistError("{klass}, alias_name:{alias_name}".format(
                klass=self.__class__.__name__,
                alias_name=self._alias_name,
            ))
        hosts = es_config["hosts"]
        http_auth = es_config["http_auth"]
        timeout = es_config["timeout"]
        client = es.Elasticsearch(
            hosts,
            http_auth=http_auth,
            verify_certs=True,
            ca_certs=certifi.where(),
            timeout=timeout
        )
        return client

    def create_index(self, body):
        index_is_exist = self.client.indices.exists(self.index_name)
        if not index_is_exist:
            self.client.indices.create(self.index_name, body)
            print(self._name)
            print(self.index_mapping_body)
        else:
            print("索引：{name} 已存在！".format(
                name=self._name
            ))

    def update_index(self):
        index_is_exist = self.client.indices.exists(self.index_name)
        if index_is_exist:
            self.index_mapping_body["mappings"][self.type_name]["properties"].update(self.default_mapping_properties)
            self.client.indices.put_mapping(self.type_name, self.index_mapping_body["mappings"], index=self.index_name)
        else:
            raise IndexCreateError("索引：{name} 不存在！".format(
                name=self._name
            ))
        print(self._name)
        print(self.index_mapping_body)

    def get_mappings(self):
        if self.index_mapping_body:
            return self.index_mapping_body[self.index_name]

    def gen_objectid(self, oid=None):
        if oid:
            object_id = oid
        else:
            object_id = str(ObjectId())
        return object_id

    def adapte_query(self, query, **kwargs):
        mode = kwargs.get("query_mode") or QueryMode.ELASTICSEARCH.value[0]
        if mode == QueryMode.ELASTICSEARCH.value[0]:
            return query
        else:
            raise QueryModeError(mode)

    def restfulapi_search(self, dsl):
        pass

    def count(self, query, **kwargs):
        if not query:
            dsl = None
        else:
            dsl = {}
            dsl["query"] = self.adapte_query(query, **kwargs)
        count = self.elasticsearch_count(dsl)
        return count

    @time_consume
    def elasticsearch_count(self, dsl):
        count = self.client.count(self.index_name, self.type_name, dsl).get("count", 0)
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


    @time_consume
    def find_one(self, id, project=None, **kwargs):
        dsl = {
            "query": {
                "term": {
                    "id":id
                }
            }
        }

        includes, excludes = self.project_handle(project)
        if includes:
            dsl.setdefault("_source", {}).update(dict(
                includes=includes,
            ))

        if excludes:
            dsl.setdefault("_source", {}).update(dict(
                excludes=excludes,
            ))

        search_result = self.elasticsearch_search(dsl, **kwargs)
        hits = search_result.get("hits", {}).get("hits", [])
        if hits:
            hit = hits[0]
            obj = {}
            obj.update(hit["_source"])

            if "_score" in includes:
                obj.update(dict(
                    _score=hit["_score"],
                ))
            if "_id" in includes:
                obj.update(dict(
                    _id=hit["_id"],
                ))
        else:
            obj = None

        return obj

    @time_consume
    def elasticsearch_search(self, dsl, **kwargs):
        search_result = self.client.search(self.index_name, self.type_name, dsl, **kwargs)
        return search_result

    @time_consume
    def elasticsearch_aggregate(self, body, query=None, **kwargs):
        dsl = {}

        if query != None:
            dsl["query"] = self.adapte_query(query, **kwargs)

        if body:
            dsl["aggs"] = body
        else:
            raise AggregateBodyError(body)

        aggs_result = self.client.search(self.index_name, self.type_name, dsl, **kwargs)
        return aggs_result

    @time_consume
    def elasticsearch_bulk(self, body, **kwargs):
        bulk_result = self.client.bulk(body, index=self.index_name, doc_type=self.type_name, refresh=True, **kwargs)
        errors = bulk_result.get("errors")
        if errors == True:
            raise Exception(bulk_result)
        return bulk_result

    def bulk_body_metadata(self, action, id):
        metadata = {action:{"_id": id}}
        if self.index_name:
            metadata[action].update(dict(
                _index = self.index_name,
            ))

        if self.type_name:
            metadata[action].update(dict(
                _type = self.type_name,
            ))

        return metadata

    def insert(self, vals, **kwargs):
        if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
            vals = self.scheme(vals)
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        self.client.index(self.index_name, self.type_name, vals, key)
        return key

    def bulk_body_create(self, vals):
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        metadata = self.bulk_body_metadata("create", key)
        body = [metadata, vals]
        return body

    def bulk_body_index(self, vals):
        if hasattr(self, "scheme") and isinstance(self.scheme, Schema):
            vals = self.scheme(vals)
        key = vals.get(self.PRIMARY_KEY) or self.gen_objectid()
        vals["id"] = key
        metadata = self.bulk_body_metadata("index", key)
        body = [metadata, vals]
        return body

    def bulk_body_delete(self, id):
        metadata = self.bulk_body_metadata("delete", id)
        body = [metadata]
        return body

    def bulk_body_update(self, id, vals):
        metadata = self.bulk_body_metadata("update", id)
        body = [metadata, {"doc": vals}]
        return body

    def search(self, query=None, sort=None, project=None, page=None, page_size=None, **kwargs):
        dsl = {}

        if query == None:
            dsl["query"] = self.match_all_query
        else:
            dsl["query"] = self.adapte_query(query, **kwargs)

        includes, excludes = self.project_handle(project)
        if includes:
            dsl.setdefault("_source", {}).update(dict(
                includes=includes,
            ))

        if excludes:
            dsl.setdefault("_source", {}).update(dict(
                excludes=excludes,
            ))

        if page != None:
            skip = self.page2skip(page, page_size)
        else:
            skip = 0
        dsl["from"] = skip

        if page_size != None:
            limit = int(page_size)
        else:
            limit = settings.PAGE_SIZE
        dsl["size"] = limit

        if sort != None:
            sort_items = sort.items()
            for item in sort_items:
                field = item[0]
                value = item[1]
                if value == 1 or value == "asc":
                    dsl.setdefault("sort", []).append({field:{"order":"asc"}})
                elif value == -1 or value == "desc":
                    dsl.setdefault("sort", []).append({field: {"order": "desc"}})
                else:
                    raise SortError(sort)

        search_result = self.elasticsearch_search(dsl)

        objs = []
        hits = search_result.get("hits", {}).get("hits", [])
        for hit in hits:
            obj = {}
            obj.update(hit["_source"])

            if "_score" in includes:
                obj.update(dict(
                    _score=hit["_score"],
                ))
            if "_id" in includes:
                obj.update(dict(
                    _id = hit["_id"],
                ))

            objs.append(obj)

        length = self.count(dsl["query"], query_mode=QueryMode.ELASTICSEARCH.value[0])
        page = self.skip2page(skip, limit)
        pager = self.count_page(length, page, page_size=limit)

        return objs, pager

    def update(self, id, vals, **kwargs):
        body = {"doc": vals}
        self.client.update(self.index_name, self.type_name, id, body=body)

    def remove(self, id, **kwargs):
        self.client.delete(self.index_name, self.type_name, id)

    def mget(self, ids, **kwargs):
        mget_result = self.client.mget({"ids":ids}, self.index_name, self.type_name, **kwargs)
        docs = mget_result.get("docs") or []
        objs = []
        for doc in docs:
            obj = doc.get("_source")
            if obj:
                objs.append(obj)
        return objs

    def aggregate(self, body, **kwargs):
        pass

    def bulk(self, body, **kwargs):
        pass


    ###############
    # 兼容server1.x版本的相关接口
    ###############

    def search_read(self, page=1, page_size=10, *args, **kwargs):
        query_params = kwargs.get("query_params")
        query = query_params["query"]

        # 排序参数
        sort = kwargs.get("sort_params") or None

        project = kwargs.get("_project") or {}

        objs, pager = self.search(query, sort, project, page, page_size, **kwargs)

        return objs, pager

    def blank_search(self,page=1,page_size=10,*args,**kwargs):
        return self.search_read(page, page_size, *args, **kwargs)
