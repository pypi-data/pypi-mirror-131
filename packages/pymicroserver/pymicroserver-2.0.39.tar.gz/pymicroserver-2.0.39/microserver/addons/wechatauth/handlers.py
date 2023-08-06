#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : handlers.py
# @Author: ZhangXiaocheng
# @Date  : 2018/8/27


import ast
import json
import time

from microserver.addons.wechatauth.models import WxUserModel
from microserver.addons.wechatauth.session import Session
from microserver.core.handlers import handlers
from microserver.utils import decorator
from microserver.utils import crypto


class AccessTokenHandler(handlers.NoAuthHandler):
    """
@name 微信认证
@path
  /wechatauth/login:
      post:
        tags:
        - "微信认证"

        description: "微信登录，获取access_token"

        parameters:
        - name: "appid"
          in: "form-data"
          description: "微信开放平台注册的应用id"
          required: true

        - name: "code"
          in: "form-data"
          description: "前端请求得到的code"
          required: true

        responses:
          200:
            description: "返回成功"
            schema:
              $ref: "#definitions/UserSessionResponseData"
          400:
            description: "参数错误"
          500:
            description: "后台处理异常"
@endpath

@definitions
  UserSessionResponseData:
    type: "object"
    required:
    - "user_session_key"
    properties:
      user_session_key:
        type: "string"
        description: "用户存token的缓存key"
@enddefinitions
    """
    model = WxUserModel()

    @decorator.handler_except
    def prepare(self):
        super(AccessTokenHandler, self).prepare()
        self.appid = self.get_argument("appid")
        self.code = self.get_argument("code")

    @decorator.threadpoll_executor
    def post(self):
        result = self.init_response_data()
        access_token_obj = self.model.get_access_token(self.appid, self.code)
        if access_token_obj.get('errcode'):
            result['code'] = 400
            result['msg'] = access_token_obj.get('errmsg', 'invalid code')
        else:
            session_key = self.appid + str(int(time.time()))
            user_session_key = crypto.md5(session_key+access_token_obj.get('openid'))
            Session().set(user_session_key, access_token_obj)
            access_token = access_token_obj['access_token']
            openid = access_token_obj['openid']
            user_info = self.model.get_user_info(access_token, openid)
            print('WeChat User\'s basic Info:', user_info)
            user_info.update(access_token_obj)
            unionid = user_info['unionid']
            user = self.model.find_one_by_query(
                {
                    'openId': openid,
                    'unionId': unionid,
                    'is_enable': True
                }
            )
            if user:
                id = user.get('id')
                self.model.save(id, user_info)
            else:
                self.model.create_wxuser(user_info)

            result['data'] = {
                'user_session_key': user_session_key
            }
        return result


class WxUserHandler(handlers.NoAuthHandler):
    """
@path
  /wechatauth/user:
      get:
        tags:
        - "微信认证"

        description: "微信登录后获取微信用户基本信息"

        parameters:
        - name: "appid"
          in: "form-data"
          description: "微信开放平台注册的应用id"
          required: true

        - name: "user_session_key"
          in: "form-data"
          description: "调用登录接口返回的user_session_key"
          required: true

        responses:
          200:
            description: "返回成功"
            schema:
              $ref: "#definitions/UserInfoResponseData"
          400:
            description: "参数错误"
          401:
            description: "认证失败，用户未登录"
          500:
            description: "后台处理异常"
@endpath

@definitions
  UserInfoResponseData:
    type: "object"
    required:
    - "openId"
    - "unionId"
    - "nickName"
    - "avatarUrl"
    - "gender"
    - "country"
    - "province"
    - "city"
    - "privilege"
    - "language"
    properties:
      openId:
        type: "string"
        description: "用户openid，普通用户的标识，对当前开发者帐号唯一"
      unionId:
        type: "string"
        description: "用户统一标识，针对一个微信开放平台帐号下的应用，同一用户的unionid唯一"
      nickName:
        type: "string"
        description: "用户微信昵称"
      avatarUrl:
        type: "string"
        description: "用户头像url"
      gender:
        type: "integer"
        description: "用户性别，1为男，2为女"
      country:
        type: "string"
        description: "国家，如中国为CN"
      province:
        type: "string"
        description: "微信用户填写的省份"
      city:
        type: "string"
        description: "微信用户填写的城市"
      priviege:
        type: "array"
        description: "用户特权信息，如微信沃卡用户为（chinaunicom）"
        items:
          type: "string"
      language:
        type: "string"
        description: "语言，如中文为zh_CN"
@enddefinitions
    """
    model = WxUserModel()

    @decorator.handler_except
    def prepare(self):
        super(WxUserHandler, self).prepare()
        self.appid = self.get_argument('appid')
        self.user_session_key = self.get_argument('user_session_key')

    @decorator.threadpoll_executor
    def get(self, *args, **kwargs):
        result = self.init_response_data()
        access_token_obj = Session().get(self.user_session_key)
        if access_token_obj is None or access_token_obj == '':
            result['code'] = 401,
            result['msg'] = '用户未登录，请重新获取access_token'
        else:
            access_token_obj = ast.literal_eval(access_token_obj)
        access_token = access_token_obj['access_token']
        openid = access_token_obj['openid']
        unionid = access_token_obj['unionid']
        refresh_token = access_token_obj['refresh_token']
        user_obj = self.model.find_one_by_query(
            {
                'openId': openid,
                'unionId': unionid,
                'is_enable': True
            }
        )
        user_id = user_obj.get('id')
        check_result = self.model.check_access_token(access_token, openid)
        if check_result.get('errcode') != 0:
            new_token_obj = self.model.refresh_access_token(self.appid, refresh_token)
            new_token_obj.update({'unionid': unionid})
            new_access_token = new_token_obj['access_token']
            # Refresh token
            Session().set(self.user_session_key, new_token_obj)
            self.model.save(user_id, {'access_token': new_access_token})
        else:
            new_access_token = access_token
        user_info = self.model.get_user_info(new_access_token, openid)
        self.model.save(user_id, user_info)

        user_info['privilege'] = ast.literal_eval(user_info['privilege'])
        result['data'] = user_info
        return result
