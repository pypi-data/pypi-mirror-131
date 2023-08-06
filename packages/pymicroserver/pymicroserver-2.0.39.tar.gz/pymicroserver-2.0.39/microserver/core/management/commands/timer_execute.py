# @Time    : 2018/8/10 15:53
# @Author  : Niyoufa
import time
import threading
from microserver.core.management.base import BaseCommand
from microserver.libs.commandlib import subprocess_popen


class Command(BaseCommand):
    """定时命令执行器"""

    def add_arguments(self, parser):
        parser.add_argument(
            "command",
            help="命令"
        )

        parser.add_argument(
            "interval",
            type=lambda x: int(x),
            help="定时间隔， 以s为单位"
        )

    def handle(self, *args, **options):
        self.command = options["command"]
        self.interval = options["interval"]
        self.timer_start()

    def execute_task(self):
        subprocess_popen(self.command)

    def timer_start(self):
        while True:
            t = threading.Timer(0, self.execute_task)
            t.start()
            time.sleep(self.interval)
