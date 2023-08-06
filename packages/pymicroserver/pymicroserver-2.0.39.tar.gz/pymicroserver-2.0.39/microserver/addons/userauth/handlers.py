from microserver.conf import settings
from microserver.core.handlers import handlers
from microserver.utils import decorator

from microserver.addons.userauth.models import UserModel, UserProfileModel
from microserver.addons.userauth.error import UserExistsError
from microserver.addons.userauth.util import check_email, check_mobile
from microserver.addons.userauth.error import AuthError


class UserExistsHandler(handlers.NoAuthHandler):
    """
@name 用户名密码认证
@path
  /userauth/exists:
    get:
      tags:
      - "用户名密码认证"
      
      description: "用户是否存在，如果不存在，可以注册"
      
      parameters:
      - name: "username"
        in: "query"
        description: "用户名"
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
    model = UserModel()

    @decorator.handler_except
    def prepare(self):
        """在请求方法 get、post等执行前调用，进行通用的参数初始化，支持协程"""
        self.username = self.get_argument("username")

    @decorator.threadpoll_executor
    def get(self, *args, **kwargs):
        """IO操作"""
        result = self.init_response_data()
        user = self.model.get_user_by_username(self.username)
        if user:
            result["data"] = dict(
                exists = True
            )
        else:
            result["data"] = dict(
                exists = False
            )
        return result


class RegisterHandler(handlers.NoAuthHandler):
    """
@path
  
  /userauth/register:
    post:
      tags:
      - "用户名密码认证"
        
      description: "注册"
        
      parameters:
      - name: "username"
        in: "form"
        description: "用户名"
        required: "true"
      - name: "password"
        in: "form"
        description: "密码"
        required: "true"
      - name: "email"
        in: "form"
        description: "邮箱"
      - name: "phone"
        in: "form"
        description: "手机"
      - name: "nickname"
        in: "form"
        description: "昵称"
        
      responses:
        200:
          description: "返回成功"
        400:
          description: "用户参数错误"
        500:
          description: "后台处理异常"

@endpath

"""
    model = UserModel()

    @decorator.handler_except
    def prepare(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        self.user_form = dict(
            username = username,
            password = password
        )

        email = self.get_argument("email", None)
        if email != None:
            check_email(email)
            self.user_form.update(dict(
                email = email
            ))

        phone = self.get_argument("phone", None)
        if phone != None:
            check_mobile(phone)
            self.user_form.update(dict(
                phone = phone
            ))

        nickname = self.get_argument("nickname", None)
        if nickname != None:
            self.user_form.update(dict(
                nickname = nickname
            ))

    @decorator.threadpoll_executor
    def post(self, *args, **kwargs):
        result = self.init_response_data()
        self.model.create_user(self.user_form)
        return result


class LoginHandler(handlers.NoAuthHandler):
    """
@path

  /userauth/login:
    post:
      tags: 
      - "用户名密码认证"

      description: "账号密码登录"

      parameters:
      - name: "username"
        in: "form"
        description: "用户名"
        required: "true"
      - name: "password"
        in: "form"
        description: "密码"
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
    model = UserModel()

    @decorator.handler_except
    def prepare(self):
        self.username = self.get_argument("username")
        self.password = self.get_argument("password")

    @decorator.threadpoll_executor
    def post(self, *args, **kwargs):
        result = self.init_response_data()
        user = self.model.get_user_by_username(self.username)
        if not self.model.check_password(user, self.password):
            raise AuthError("密码错误")

        self.model.login(user, self)

        if settings.DEBUG:
            print(self.xsrf_token)
        return result

class LogoutHandler(handlers.BaseHandler):
    """
@path

  /userauth/logout:
    post:
      tags:
      - "用户名密码认证"
    
      description: "登出"

      responses:
        200:
          description: "返回成功"
        500:
          description: "后台处理异常"

@endpath

"""
    model = UserModel()

    @decorator.threadpoll_executor
    def post(self, *args, **kwargs):
        result = self.init_response_data()
        self.model.logout(self)
        return result


class CurrentLoginUserInfoHandler(handlers.BaseHandler):
    """
@path

  /userauth/userinfo:
    get:
      tags: 
      - "用户名密码认证"
        
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
    model = UserProfileModel()

    @decorator.threadpoll_executor
    def get(self, *args, **kwargs):
        result = self.init_response_data()
        result["data"] = self.model.get_current_user(self)
        if settings.DEBUG:
            print(self.xsrf_token)
        return result


class AlterLoginPasswordHandler(handlers.BaseHandler):
    """
    
@path

  /userauth/password:
    put:
      tags: 
      - "用户名密码认证"
        
      description: "修改当前登录用户密码"
      
      parameters:
      - name: "old_password"
        in: "form"
        description: "原密码"
        required: "true"
      - name: "new_password"
        in: "form"
        description: "新密码"
        required: "true"
      
      responses:
        200:
          description: "返回成功"
        500:
          description: "后台处理异常"

@endpath

"""
    model = UserModel()

    @decorator.handler_except
    def prepare(self):
        super(AlterLoginPasswordHandler, self).prepare()

        self.old_password = self.get_argument("old_password")
        self.new_password = self.get_argument("new_password")

    @decorator.threadpoll_executor
    def put(self, *args, **kwargs):
        result = self.init_response_data()
        username = self.get_current_user()
        user = self.model.get_user_by_username(username)
        if not self.model.check_password(user, self.old_password):
            raise AuthError("密码错误")
        if self.old_password == self.new_password:
            raise self.ArgumentTypeError("新密码与旧密码相同")

        # 修改密码并登出
        self.model.set_password(user, self.new_password)
        self.model.logout(self)
        return result
