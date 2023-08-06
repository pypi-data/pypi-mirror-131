# @Time    : 2018/9/5 16:17
# @Author  : Niyoufa
from microserver.addons.command.handlers import CommandExecuteHandler, \
    CommandsHandler


handlers = [
    (r"/commands$", CommandsHandler),
    (r"/commands/(?P<command_name>[a-zA-Z0-9_]+)$", CommandsHandler),
    (r"/command/execute$", CommandExecuteHandler),
]