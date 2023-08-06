# @Time    : 2018/4/2 10:50
# @Author  : Niyoufa
from microserver.addons.siege.handlers import *

handlers = [
    (r"/siege", SiegeHandler),
]