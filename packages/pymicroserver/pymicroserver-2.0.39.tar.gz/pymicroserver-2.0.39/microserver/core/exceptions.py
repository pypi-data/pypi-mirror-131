# @Time    : 2018/3/12 17:48
# @Author  : Niyoufa
from tornado.web import HTTPError


class HandlerError(HTTPError):
    """请求响应处理异常类, 继承该异常类的异常会被全局捕捉，详见utils/decorator.py"""


class ArgumentTypeError(HandlerError):
    """参数类型错误"""

    def __init__(self, arg_name):
        super(ArgumentTypeError, self).__init__(
            400, '%s' % arg_name)
        self.arg_name = arg_name
        self.reason = '%s' % arg_name


class MissingArgumentError(HandlerError):
    """缺失请求参数错误"""

    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            400, '缺失请求参数 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '缺失请求参数 %s' % arg_name

class EnumError(HandlerError):
    """枚举异常"""

    def __init__(self, arg_name):
        super(EnumError, self).__init__(
            400, '枚举参数错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '枚举参数错误 %s' % arg_name

class AuthError(HandlerError):
    """认证错误"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            401, '认证错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '认证错误 %s' % arg_name