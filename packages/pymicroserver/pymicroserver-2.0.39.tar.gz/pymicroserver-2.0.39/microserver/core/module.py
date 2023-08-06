# @Time    : 2018/3/20 14:07
# @Author  : Niyoufa
import sys
import traceback
from microserver.conf import settings
from microserver.libs.singletonlib import Singleton


class ModuleNotExistsError(Exception):
    """
    模块不存在错误
    """


class Module(object):
    """
    模块
    """

    def __init__(self, module):
        self.module = module
        self.handlers = self.load_module()

    def load_module(self):
        hanlders = []
        try:
            __import__(self.module)
            module_obj = sys.modules[self.module]
            module_hanlders = getattr(module_obj, "handlers", None)
            if isinstance(module_hanlders, list):
                hanlders.extend(module_hanlders)
        except ImportError:
            info = traceback.format_exc()
            raise ModuleNotExistsError("{module} load error, {info}".format(module=self.module, info=info))

        return hanlders

    def print_handlers(self):
        print("'{module}'".format(module=self.module))
        for handler in self.handlers:
            print(handler[0])


class ModuleManager(Singleton):
    """模块管理器"""

    def __init__(self):
        self.modules = []
        for module in settings.MODULES:
            module_obj = Module(module)
            self.modules.append(module_obj)

    def get_handlers(self):
        handlers = []
        for module in self.modules:
            module.print_handlers()
            handlers.extend(module.handlers)
        return handlers

    def gen_swagger_apidoc(self):
        handlers = self.get_handlers()
        for handler in handlers:
            print(handler)

