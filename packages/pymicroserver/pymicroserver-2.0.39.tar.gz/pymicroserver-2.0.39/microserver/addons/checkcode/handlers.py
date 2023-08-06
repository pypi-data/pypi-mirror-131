import datetime

from microserver.core.handlers.handlers import NoAuthHandler
from microserver.utils import decorator
from microserver.addons.checkcode.models import CheckCode


class MobileCheckCode(NoAuthHandler):
    model = CheckCode()

    @decorator.threadpoll_executor
    def get(self):
        result = self.init_response_data()
        checkcode_coll = self.model.get_coll()
        mobile = self.get_argument("phone")
        self.model.check_mobile(mobile)
        curr_time = datetime.datetime.now()
        if checkcode_coll.find({"mobile":mobile,"is_enable":True}).count() > 0:
            # 验证码请求限制 每小时限制5条
            if checkcode_coll.find({"mobile":mobile,
                    "add_time":{
                        "$gte":curr_time - datetime.timedelta(hours=1),
                        "$lte":curr_time + datetime.timedelta(hours=1),
                    }
                }).count() >= 5:
                raise self.ArgumentTypeError("验证码请求限制，每小时限制5条！")

            cr = checkcode_coll.find({"mobile":mobile,"is_enable":True})
            for checkcode in cr:
                checkcode["is_enable"] = False
                checkcode_coll.save(checkcode)
        else:
            pass
        random_code = self.model.get_random_num(6,mode="number")

        checkcode_coll.insert_one({
            "mobile":mobile,
            "is_enable":True,
            "add_time":curr_time,
            "type":"mobile",
            "code":random_code,
        })
        #发送短信验证码
        self.model.send_checkcode(mobile, random_code, handler=self)
        return result

    @decorator.threadpoll_executor
    def post(self):
        result = self.init_response_data()
        phone = self.get_argument("phone","")
        phone_code = self.get_argument("phone_code","")
        if phone != "":
            self.model.check_code(phone, phone_code)
        return result