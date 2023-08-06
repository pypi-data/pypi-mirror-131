from microserver.addons.userauth.handlers import *

handlers = [
    (r"/userauth/exists", UserExistsHandler),
    (r"/userauth/register", RegisterHandler),
    (r"/userauth/login", LoginHandler),
    (r"/userauth/logout", LogoutHandler),
    (r"/userauth/userinfo", CurrentLoginUserInfoHandler),
    (r"/userauth/password", AlterLoginPasswordHandler),
]