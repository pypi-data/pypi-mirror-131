# @Time    : 2018/5/18 16:18
# @Author  : Niyoufa
from microserver.core.management.base import BaseCommand
from microserver.addons.swagger.api import SwaggerManager


class Command(BaseCommand):
    """
    生成接口文档
    """

    def handle(self, *args, **options):
        swagger_manager = SwaggerManager()
        swagger_manager.create_apidoc()