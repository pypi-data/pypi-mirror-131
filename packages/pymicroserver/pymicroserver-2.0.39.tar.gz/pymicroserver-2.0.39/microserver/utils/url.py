# @Time    : 2018/4/2 11:13
# @Author  : Niyoufa
import re
from urllib import parse

def validate(url):
    regex = "^(https?)://.+$"
    if not re.match(regex, url):
        raise Exception("url format error： {url}".format(url=url))

def get_url_parse_result(url):
    validate(url)
    parse_result_obj = parse.urlparse(url)
    parse_result = dict(
        scheme = parse_result_obj.scheme,
        hostname = parse_result_obj.hostname,
        path = parse_result_obj.path,
        query = parse_result_obj.query,
        username = parse_result_obj.username,
        password = parse_result_obj.password,
        port = parse_result_obj.port,
        params = parse_result_obj.params,
        params_dict = parse.parse_qs(parse_result_obj.query)
    )
    return parse_result