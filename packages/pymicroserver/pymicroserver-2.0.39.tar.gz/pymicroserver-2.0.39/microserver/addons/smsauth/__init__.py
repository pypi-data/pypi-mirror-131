# @Time    : 2018/6/28 14:30
# @Author  : Niyoufa
from microserver.addons.smsauth.handlers import *

handlers = [
    (r"/smsauth/exists", UserExistsHandler),
    (r"/smsauth/login", LoginHandler),
    (r"/smsauth/register", RegisterHandler),
    (r"/smsauth/userinfo", SmsCurrentLoginUserInfoHandler),
]