# @Time    : 2018/3/12 15:33
# @Author  : Niyoufa
import tornado.web
import tornado.concurrent
import tornado.httpserver
import tornado.ioloop

from microserver.conf import settings as const_settings
from microserver.core.module import ModuleManager


class Application(tornado.web.Application):

    def __init__(self, **kwargs):

        settings = dict(
            debug = const_settings.DEBUG,
            autoreload = const_settings.AUTORELOAD,
            cookie_secret = const_settings.COOKIE_SECRET,
            xsrf_cookies = const_settings.XSRF_COOKIES,
        )

        static_path = const_settings.get_static_absolute_path()
        if static_path:
            settings.update(dict(static_path=static_path))

        template_path = const_settings.get_template_absolute_path()
        if template_path:
            settings.update(dict(template_path=template_path))

        redis_config = const_settings.get_redis_config(kwargs.get("redis"))
        if redis_config:
            settings.update(dict(pycket={
                'engine': 'redis',
                'storage': {
                    'host': redis_config["host"],
                    'port': redis_config["port"],
                    'db_sessions': redis_config["db_sessions"],
                    'db_notifications': redis_config["db_notifications"],
                    'max_connections': redis_config["max_connections"],
                },
                'cookies': {
                    'expires_days': 7,
                    # 'expires':None, #秒
                },
            }))
        handlers = ModuleManager().get_handlers()
        super(Application, self).__init__(handlers, **settings)
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor()
