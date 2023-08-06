# @Time    : 2018/7/19 11:20
# @Author  : Niyoufa
import time
from microserver.db.mongodb import MongoDB
from microserver.conf import settings
from microserver.utils.decorator import ip_limit


class SmsUserModel(MongoDB):
    _name = "smsuser.user"
    _alias_name = "mongodb"

    def create(self, vals, **kwargs):
        phone = vals["phone"]

        if self.find_one_by_query({"phone": phone}):
            raise self.ArgumentTypeError("手机号已被注册")

        obj = dict(
            phone = phone,
            is_enable = True
        )
        return self.insert(obj, **kwargs)

    # @ip_limit
    def login(self, **kwargs):
        handler = kwargs["handler"]
        user = kwargs["user"]
        phone = user["phone"].encode()
        user_id = str(user["id"]).encode()

        # 登录状态过期设置
        if "login_expires_days" in settings.USERAUTH:
            login_expires_days = settings.USERAUTH["login_expires_days"]

            handler.set_secure_cookie('username', phone,
                                      expires_days=login_expires_days)

            handler.set_secure_cookie("user_id", user_id,
                                      expires_days=login_expires_days)

        elif "login_expires" in settings.USERAUTH:
            login_expires = int(settings.USERAUTH["login_expires"])

            handler.set_secure_cookie('username', phone,
                                      expires=int(time.time() + login_expires))

            handler.set_secure_cookie("user_id", user_id,
                                      expires=int(time.time() + login_expires))

        else:
            handler.set_secure_cookie('username', phone)
            handler.set_secure_cookie("user_id", user_id)

        # token 过期设置
        if "csrf_expires_days" in settings.USERAUTH:
            csrf_expires_days = settings.USERAUTH["csrf_expires_days"]

            handler.set_cookie("csrf_token", handler.xsrf_token,
                               expires_days=csrf_expires_days)

        elif "csrf_expires" in settings.USERAUTH:
            csrf_expires = int(settings.USERAUTH["csrf_expires"])

            handler.set_cookie("csrf_token", handler.xsrf_token,
                               expires=int(time.time() + csrf_expires))

        else:
            handler.set_cookie("csrf_token", handler.xsrf_token)

    def logout(self, handler):
        handler.clear_all_cookies()

    def get_current_user(self, handler):
        phone = handler.get_secure_cookie("username")
        if not phone:
            raise handler.AuthError("用户未登录")
        else:
            phone = phone.decode()

        query = {"phone": phone}

        user = self.find_one_by_query(query, project={"_id":0, "is_enable": 0})
        return user

