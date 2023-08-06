# @Time    : 2018/3/31 下午5:29
# @Author  : Niyoufa
from enum import IntEnum

__all__ = ['HTTPStatus']

class HTTPStatus(IntEnum):

    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    # server errors
    HTTPError = 599, 'Timeout', 'Timeout'
