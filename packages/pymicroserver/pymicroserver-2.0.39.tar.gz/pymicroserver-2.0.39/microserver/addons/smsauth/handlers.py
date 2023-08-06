# @Time    : 2018/6/28 14:30
# @Author  : Niyoufa
from microserver.conf import settings
from microserver.core.handlers.handlers import BaseHandler, NoAuthHandler
from microserver.addons.userauth.handlers import CurrentLoginUserInfoHandler
from microserver.addons.userauth.handlers import LogoutHandler
from microserver.addons.checkcode.handlers import MobileCheckCode
from microserver.utils import decorator
from microserver.addons.smsauth.models import SmsUserModel
from microserver.addons.checkcode.models import CheckCode


class UserExistsHandler(NoAuthHandler):
    """
@name 手机验证码认证
@path
  /intelligentpretrial/smsauth/exists:
    get:
      tags:
      - "手机验证码认证"

      description: "用户是否存在，如果不存在，可以注册"

      parameters:
      - name: "phone"
        in: "query"
        description: "用户手机号"
        required: "true"

      responses:
        200:
          description: "用户不存在, 可以注册"
        400:
          description: "用户已存在"
        500:
          description: "后台处理异常"

@endpath


"""
    model = SmsUserModel()

    @decorator.threadpoll_executor
    def get(self):
        result = self.init_response_data()
        phone = self.get_argument("phone")
        user = self.model.coll.find_one({"phone": phone, "is_enable": True})
        if user:
            result["data"] = dict(
                exists = True
            )
        else:
            result["data"] = dict(
                exists = False
            )
        return result


class SmsMobileCheckCode(MobileCheckCode):
    """
@path

  /intelligentpretrial/checkcode/mobile/checkcode:
    post:
      tags:
      - "手机验证码认证"

      description: "获取手机验证码"
      
      parameters:
      - name: "phone"
        in: "query"
        description: "用户手机号"
        required: "true"

      responses:
        200:
          description: "返回成功"
        500:
          description: "后台处理异常"

@endpath

"""


class RegisterHandler(NoAuthHandler):
    """
@path

  /intelligentpretrial/smsauth/register:
    post:
      tags:
      - "手机验证码认证"

      description: "注册"

      parameters:
      - name: "phone"
        in: "form"
        description: "用户手机号"
        required: "true"
      - name: "phone_code"
        in: "form"
        description: "手机验证码"
        required: "true"

      responses:
        200:
          description: "返回成功"
        400:
          description: "用户参数错误"
        500:
          description: "后台处理异常"

@endpath

"""
    model = SmsUserModel()
    checkcode_model = CheckCode()

    @decorator.threadpoll_executor
    def post(self):
        result = self.init_response_data()
        phone = self.get_argument("phone")
        phone_code = self.get_argument("phone_code")
        user = self.model.coll.find_one({"phone": phone, "is_enable": True})
        if not user:
            self.checkcode_model.check_mobile(phone)
            self.checkcode_model.check_code(phone, phone_code)
            self.model.create(dict(
                phone=phone
            ))
        else:
            raise self.ArgumentTypeError("用户已存在")
        return result


class LoginHandler(NoAuthHandler):
    """
@path

  /intelligentpretrial/smsauth/login:
    post:
      tags: 
      - "手机验证码认证"

      description: "手机验证码登录"

      parameters:
      - name: "phone"
        in: "form"
        description: "手机号"
        required: "true"
      - name: "phone_code"
        in: "form"
        description: "手机验证码"
        required: "true"

      responses:
        200:
          description: "返回成功"
        400:
          description: "用户参数错误"
        401:
          description: "认证错误"
        500:
          description: "后台处理异常" 

@endpath

"""
    model = SmsUserModel()
    checkcode_model = CheckCode()

    @decorator.threadpoll_executor
    def post(self):
        result = self.init_response_data()
        phone = self.get_argument("phone")
        phone_code = self.get_argument("phone_code")
        user = self.model.coll.find_one({"phone":phone, "is_enable":True})
        if not user:
            raise self.ArgumentTypeError("用户不存在！")
        else:
            self.checkcode_model.check_mobile(phone)
            self.checkcode_model.check_code(phone, phone_code)

            self.model.login(handler=self, user=user)
        return result


class SmsLogoutHandler(LogoutHandler):
    """
@path

  /intelligentpretrial/smsauth/logout:
    post:
      tags:
      - "手机验证码认证"

      description: "登出"

      responses:
        200:
          description: "返回成功"
        500:
          description: "后台处理异常"

@endpath

"""


class SmsCurrentLoginUserInfoHandler(CurrentLoginUserInfoHandler):
    """
@path

  /intelligentpretrial/smsauth/userinfo:
    get:
      tags: 
      - "手机验证码认证"

      description: "当前登录用户信息"

      responses:
        200:
          description: "返回成功"
          schema:
            $ref: "#definitions/CurrentLoginUserInfoResponseData"
        500:
          description: "后台处理异常"

@endpath

@definitions

  CurrentLoginUserInfoResponseData:
    type: "object"
    required:
    - "id"
    - "phone"
    properties:
      id:
        type: "string"
        description: "手机号用户id"
    
      phone:
        type: "string"
        description: "手机号"
        
@enddefinitions

"""
    model = SmsUserModel()
