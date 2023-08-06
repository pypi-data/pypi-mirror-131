#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : __init__.py
# @Author: ZhangXiaocheng
# @Date  : 2018/8/27

from microserver.addons.wechatauth.handlers import *

handlers = [
    (r"/wechatauth/login", AccessTokenHandler),
    (r"/wechatauth/user", WxUserHandler),
]