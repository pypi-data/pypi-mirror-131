# @Time    : 2018/3/23 15:24
# @Author  : Niyoufa
import urllib.parse
from tornado import gen
from tornado import httpclient


class HTTPError(Exception):
    pass

def _get_client(use_proxy=False):
    if use_proxy == True:
        httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    client = httpclient.AsyncHTTPClient()
    return client

@gen.coroutine
def fetch(url, **kwargs):
    http_client = _get_client()
    try:
        response = yield http_client.fetch(url, **kwargs)
    except httpclient.HTTPError as err:
        raise HTTPError("接口调用报错:{url}, {kwargs}, {err}".format(
            url = url,
            kwargs = kwargs,
            err = err
        ))
    return response

@gen.coroutine
def get(url, params=None, **kwargs):
    if params and isinstance(params, dict):
        url += "?"
        url += urllib.parse.urlencode(params)
    response = yield fetch(url, **kwargs)
    return response

@gen.coroutine
def gets(urls, **kwargs):
    http_client = _get_client()
    responses = yield [http_client.fetch(url, **kwargs) for url in urls]
    return responses

async  def async_fetch(url, **kwargs):
    http_client = _get_client()
    try:
        response = await http_client.fetch(url, **kwargs)
    except httpclient.HTTPError as err:
        raise HTTPError("接口调用报错:{url}, {kwargs}, {err}".format(
            url = url,
            kwargs = kwargs,
            err = err
        ))
    return response

async def async_get(url, params=None, **kwargs):
    if params and isinstance(params, dict):
        url += "?"
        url += urllib.parse.urlencode(params)

    response = await async_fetch(url, **kwargs)
    return response