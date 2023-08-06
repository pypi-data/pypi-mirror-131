# @Time    : 2018/3/12 16:41
# @Author  : Niyoufa

class ConstError(TypeError):
    pass


class ConstCaseError(ConstError):
    pass


class ConstSettingNotExistError(ConstError):
    pass


class _Const(object):

    def __setattr__(self, name, value):
        if not name.isupper():
            raise ConstCaseError(
                'const name "%s" is not all uppercase' %
                name)
        if name in self.__dict__:
            raise ConstError("can't change const %s" % name)
        self.__dict__[name] = value

    def __getattr__(self, item):
        if item not in self.__dict__:
            raise ConstError("const {item} not exists".format(item=item))
        else:
            return super(_Const, self).__getattribute__(item)

    def __delattr__(self, item):
        if item not in self.__dict__:
            raise ConstError("const {item} not exists".format(item=item))
        else:
            del self.__dict__[item]


const = _Const()
