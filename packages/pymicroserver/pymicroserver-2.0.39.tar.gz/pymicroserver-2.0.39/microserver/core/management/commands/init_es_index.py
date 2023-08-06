# @Time    : 2018/7/6 15:06
# @Author  : Niyoufa
import importlib
from microserver.core.management.base import BaseCommand


class Command(BaseCommand):
    """初始化当前项目es索引"""

    def add_arguments(self, parser):
        parser.add_argument(
            "module",
            help="索引Model类所在包路径",
        )
        parser.add_argument(
            "indexs",
            help = "以‘，’号分割的索引Model类名称",
            type = lambda x:[index.strip() for index in x.split(",") if index.strip()]
        )

    def handle(self, *args, **options):
        module = options["module"].strip()
        module_obj = importlib.import_module(module)

        indexs = options.get("indexs") or []
        for index in indexs:
            index_klass = getattr(module_obj, index)
            index_klass().create_index()