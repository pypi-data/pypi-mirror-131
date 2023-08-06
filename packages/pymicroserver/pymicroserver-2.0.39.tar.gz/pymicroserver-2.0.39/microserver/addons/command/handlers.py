# @Time    : 2018/9/5 16:17
# @Author  : Niyoufa
import shlex
from collections import defaultdict
from microserver.utils import decorator
from microserver.core.handlers.handlers import BaseHandler
from microserver.core.management import ManagementUtility
from microserver.core.management import execute_from_command_line
from microserver.core.management.base import BaseCommand


class CommandsHandler(BaseHandler):
    """命令列表"""

    @decorator.threadpoll_executor
    def get(self, *args, **kwargs):
        result = self.init_response_data()
        command_name = kwargs.get("command_name")
        if command_name:
            utility = ManagementUtility(["manage.py", "help", command_name])
            command_obj = utility.fetch_command(command_name)
            parser = command_obj.create_parser(utility.prog_name, command_name)
            result["data"] = [line.strip() for line in parser.format_help().split("\n")]
        else:
            commands = BaseCommand.get_commands()
            commands_dict = defaultdict(lambda: [])
            for name, apps in iter(commands.items()):
                print(name, apps)
                for app in apps.keys():
                    print(app)
                    commands_dict[name].append(app)
            result["data"] = commands_dict
        return result


class CommandExecuteHandler(BaseHandler):
    """执行命令"""

    def prepare(self):
        self.command  = self.get_argument("command")

    @decorator.threadpoll_executor
    def post(self, *args, **kwargs):
        result = self.init_response_data()

        argv = shlex.split(self.command)

        execute_from_command_line(argv[1:])

        return result