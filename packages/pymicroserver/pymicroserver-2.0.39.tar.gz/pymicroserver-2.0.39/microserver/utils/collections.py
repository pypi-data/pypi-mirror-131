# @Time    : 2018/4/17 16:22
# @Author  : Niyoufa
from enum import Enum
from microserver.core.exceptions import EnumError


class ConstDict(dict):

    def __setitem__(self, key, value):
        if key in self:
            raise Exception("can not alter ConstDict")


class BaseEnum(Enum):

    @classmethod
    def check(cls, value):
        values = [obj.value[0] for obj in list(cls.__members__.values())]
        if value not in values:
            raise EnumError("{enum}:{value}: 不存在".format(
                value=value,
                enum = cls.__name__
            ))

    @classmethod
    def get_value_dict(cls):
        value_dict = {}
        for obj in list(cls.__members__.values()):
            value_dict.update({obj.value[0]:obj.value[1]})
        return value_dict