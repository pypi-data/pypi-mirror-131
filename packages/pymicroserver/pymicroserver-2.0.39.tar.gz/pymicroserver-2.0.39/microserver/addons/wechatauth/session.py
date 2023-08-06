#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : session.py
# @Author: ZhangXiaocheng
# @Date  : 2018/8/31


import json
import time

from microserver.cache.rediscache import RedisCache


# 微信小程序用户session
class Session(RedisCache):
    alias_name = 'redis'
    pattern = 'microserver_wxauth_'
