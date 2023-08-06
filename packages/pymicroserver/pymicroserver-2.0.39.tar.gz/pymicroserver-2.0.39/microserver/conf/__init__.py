# @Time    : 2018/4/8 14:41
# @Author  : Niyoufa
import os
import importlib
from microserver.libs.singletonlib import Singleton
from microserver.libs.constlib import _Const
from microserver.libs.constlib import ConstError

ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


class _Settings(Singleton):
    __const = _Const()
    __consts = []

    def __init__(self):

        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            settings_module = "microserver.conf.default_settings"

        setattr(_Settings.__const, ENVIRONMENT_VARIABLE, settings_module)

        settings = importlib.import_module(settings_module)
        for setting in dir(settings):
            if setting.isupper():
                setting_value = getattr(settings, setting)
                setattr(_Settings.__const, setting, setting_value)
                _Settings.__consts.append((setting, setting_value))

    def __setattr__(self, name, value):
        raise ConstError("can not add new const to settings ")

    def __getattr__(self, item):
        if item not in self.__const.__dict__:
            raise ConstError("const {item} not exists in settings".format(item=item))
        else:
            return _Settings.__const.__getattribute__(item)

    def __delattr__(self, item):
        raise ConstError("can not delete const in settings")


    def get_static_absolute_path(self):
        static_path = self.STATIC or ""
        if static_path and not static_path.endswith("/"):
            static_path += "/"
        return os.path.join(self.BASE_DIR, static_path + "static")

    def get_template_absolute_path(self):
        template_path = self.TEMPLATE or ""
        if template_path and not template_path.endswith("/"):
            template_path += "/"
        return os.path.join(self.BASE_DIR, template_path + "templates")

    def get_redis_config(self, alias):
        DATABASES = self.DATABASES
        redis_configs = {}
        for k, v in DATABASES.items():
            if v.get("type") == "redis":
                redis_configs.update({k:v})
        return redis_configs.get(alias)

settings = _Settings()
