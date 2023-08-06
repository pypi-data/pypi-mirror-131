# @Time    : 2018/4/7 上午11:02
# @Author  : Niyoufa
import importlib
import string

import tornado.options
tornado.options.parse_command_line()

from tornado import httpserver
from tornado import ioloop

from microserver.conf import settings
from microserver.core.management.base import BaseCommand
from microserver.libs.constlib import ConstSettingNotExistError
from microserver.core.app import Application


class Command(BaseCommand):
    """
    启动服务器
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'port',
            help='端口',
        )
        parser.add_argument(
            '--num_processes',
            default=1,
            help='进程数'
        )

        parser.add_argument(
            '--redis',
            default="redis",
            help='redis配置'
        )

        parser.add_argument(
            '--logging',
            default="debug, choices is debug|info|warning|error|none",
            help='使用tornado.log.access_log打印日志'
        )

    def handle(self, *args, **options):
        if not settings.SETTINGS_MODULE:
            raise ConstSettingNotExistError("can't find settings.py file")

        cache_names = [cache_name for cache_name, flag in settings.CACHES.items() if flag]
        for cache_name in cache_names:
            cache_module = importlib.import_module(cache_name)
            klass = getattr(cache_module, "".join([string.capwords(word) for word in cache_name.split(".")[-1].split("_")]))
            klass().init_cache()

        port = options["port"]
        num_processes = int(options["num_processes"])

        app = Application(**options)

        http_server = httpserver.HTTPServer(app)
        http_server.bind(port)
        http_server.start(num_processes)
        ioloop.IOLoop.current().add_callback(
            lambda: print("server start, port: {port}!".format(port=port)))
        ioloop.IOLoop.current().start()
