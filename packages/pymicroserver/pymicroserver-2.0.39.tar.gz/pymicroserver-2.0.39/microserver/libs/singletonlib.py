# @Time    : 2018/3/23 15:25
# @Author  : Niyoufa

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance