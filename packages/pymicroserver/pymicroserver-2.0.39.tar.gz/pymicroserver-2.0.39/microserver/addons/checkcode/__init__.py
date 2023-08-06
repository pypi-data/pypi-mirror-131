# @Time    : 2018/6/28 14:30
# @Author  : Niyoufa
from microserver.addons.checkcode.handlers import *
handlers = [
    (r"/checkcode/mobile/checkcode", MobileCheckCode),
    (r"/checkcode/mobile/check", MobileCheckCode),
]