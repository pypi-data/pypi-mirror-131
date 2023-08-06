# @Time    : 2018/6/15 14:18
# @Author  : Niyoufa
from microserver.core.exceptions import HandlerError


class UserExistsError(HandlerError):
    """用户已存在异常"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            400, '用户已存在 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '用户已存在 %s' % arg_name

class UserNotExists(HandlerError):
    """用户不存在"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            400, '用户不存在 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '用户不存在 %s' % arg_name

class AuthPasswordError(HandlerError):
    """密码认证错误"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            401, '密码错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '密码错误 %s' % arg_name

class AuthError(HandlerError):
    """认证错误"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            401, '认证错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '认证错误 %s' % arg_name