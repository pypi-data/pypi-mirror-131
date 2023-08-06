#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/31 18:22
# @Author  : Niyoufa
# @Site    :
# @File    : proxy.py.py
# @Software: PyCharm
# document https://www.abuyun.com/http-proxy/pro-manual-python.html
import base64
from microserver.conf import settings
proxy = settings.PROXY
proxyHost = proxy["proxyHost"]
proxyPort = proxy["proxyPort"]
proxyUser = proxy["proxyUser"]
proxyPass = proxy["proxyPass"]

proxyServer = "%s:%s"%(proxyHost, proxyPort)
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}
