# @Time    : 2018/4/20 下午10:30
# @Author  : Niyoufa
from voluptuous import (
    Schema, Required, Invalid
)
from microserver.core.exceptions import HandlerError


class ResponseFormatError(HandlerError):
    """接口响应数据格式错误"""

    def __init__(self, arg_name):
        super(ResponseFormatError, self).__init__(
            500, '接口响应数据格式错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '接口响应数据格式错误 %s' % arg_name


class ResponseScheme(object):
    schema = Schema({
        Required("code"): int,
        Required("msg"): str,
        "data": dict
    })

    def __call__(self, res):
        try:
            return self.schema(res)
        except Invalid:
            raise ResponseFormatError(res)
