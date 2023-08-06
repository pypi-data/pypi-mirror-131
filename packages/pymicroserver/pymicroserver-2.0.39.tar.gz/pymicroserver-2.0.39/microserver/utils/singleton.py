# @Time    : 2018/4/7 下午6:01
# @Author  : Niyoufa


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance