import random
import string
import datetime
import time
import json
import requests
from microserver.db.mongodb import MongoDB
from microserver.conf import settings
from microserver.utils.crypto import md5


class CheckCode(MongoDB):
    _name = "checkcode.checkcode"
    _alias_name = "mongodb"

    def send_checkcode(self,mobile,code, **kwargs):
        appid = "api_server"
        secret = "5a70d603-b820-4724-a222-abab79a477ba"
        timestamp = int(time.time() * 1000)
        headers = {"appid":"api_server", "key":md5(appid + secret + str(timestamp)), "time":str(timestamp)}
        data = {"content":"%s(验证码十分钟内有效)"%code, "numbers":json.dumps({mobile:"小法问答"}),
                "user_id":"123", "app":"test", "schedule":0, "attach":{}}
        try:
            result = requests.post(settings.SMS_URL, headers=headers, data=data).text
            code = json.loads(result).get("code")
        except Exception as err:
            raise self.ArgumentTypeError("短信发送失败: %s"%err.args)

        if code != 0:
            raise self.ArgumentTypeError(result)

    def check_mobile(self,mobile):
        if len(mobile) != 11:
            raise Exception("手机号必须是11位数字！")
        else:
            if not mobile.isdigit():
                raise self.ArgumentTypeError("手机号必须是数字！")

    def get_random_num(self, length, mode='string'):
        if mode == 'string':
            return ''.join([(string.ascii_letters + string.digits)[x] for x in random.sample(range(0, 62), length)])
        elif mode == 'number':
            return ''.join([(string.digits)[x] for x in random.sample(range(0, 10), length)])

    def check_code(self, str, code, type="mobile"):
        # 测试用验证码
        if settings.DEBUG and code == "920816":
            return
        else:
            if type == "mobile":
                checkcode = self.coll.find_one({"mobile": str, "code": code, "is_enable": True})
                # 验证码的有效时间
                if checkcode:
                    if code.upper() != checkcode["code"].upper():
                        raise self.ArgumentTypeError("手机验证码错误！")
                    elif checkcode["add_time"] <= datetime.datetime.now() - datetime.timedelta(minutes=10):
                        raise self.ArgumentTypeError("手机验证码过期！")
                    checkcode["is_enable"] = False
                    self.coll.save(checkcode)
                else:
                    raise self.ArgumentTypeError("手机验证码错误")
            elif type == "email":
                raise self.ArgumentTypeError("暂不支持！")
            else:
                raise self.ArgumentTypeError("验证码类型错误！")
