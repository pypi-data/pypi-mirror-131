#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : models.py
# @Author: ZhangXiaocheng
# @Date  : 2018/8/27


import json
import requests

from microserver.conf import settings
from microserver.db.mysql import MySQL, Base, Column, CHAR, TEXT, \
    UniqueConstraint, Boolean, DateTime, Integer, BIGINT


class WxUserModel(Base, MySQL):
    """
    微信用户表
    """

    __tablename__ = "wx_user"
    __table_args__ = (
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    openId = Column(TEXT, nullable=False, unique=True)
    unionId = Column(TEXT, nullable=False)
    access_token = Column(TEXT, nullable=False)
    expires_in = Column(Integer, nullable=False)
    refresh_token = Column(TEXT, nullable=False)
    scope = Column(TEXT, nullable=False)
    nickName = Column(CHAR(length=255), nullable=False)
    country = Column(CHAR(length=255), nullable=False)
    province = Column(CHAR(length=255), nullable=False)
    city = Column(CHAR(length=255), nullable=False)
    gender = Column(Integer, nullable=False)
    avatarUrl = Column(TEXT, nullable=False)
    privilege = Column(TEXT, nullable=False)
    language = Column(CHAR(length=255), nullable=False)

    def create_wxuser(self, wxuser_form):
        openid = wxuser_form['openid']
        unionid = wxuser_form['unionid']
        nickname = wxuser_form['nickname']
        sex = wxuser_form['sex']
        country = wxuser_form['country']
        province = wxuser_form['province']
        city = wxuser_form['city']
        avatarurl = wxuser_form['headimgurl']
        privilege = json.dumps(wxuser_form['privilege'])
        access_token = wxuser_form['access_token']
        expires_in = wxuser_form['expires_in']
        refresh_token = wxuser_form['refresh_token']
        scope = wxuser_form['scope']
        language = wxuser_form['language']

        return self.insert(dict(
            openId = openid,
            unionId = unionid,
            nickName = nickname,
            gender = sex,
            country = country,
            province = province,
            city = city,
            avatarUrl = avatarurl,
            privilege = privilege,
            access_token = access_token,
            expires_in = expires_in,
            refresh_token = refresh_token,
            scope = scope,
            language = language
        ))

    def save(self, id, vals):
        vals['avatarUrl'] = vals.pop('headimgurl')
        vals['openId'] = vals.pop('openid')
        vals['unionId'] = vals.pop('unionid')
        vals['nickName'] = vals.pop('nickname')
        vals['gender'] = vals.pop('sex')
        vals['privilege'] = json.dumps(vals['privilege'])
        self.update(id, vals)

    def get_access_token(self, appid, code):
        response = requests.get(
            url=settings.WXAUTH["WX_ACCESS_TOKEN_URL"],
            params={
                'appid': appid,
                'secret': settings.WXAUTH["APPS"][appid]["secret"],
                'code': code,
                'grant_type': settings.WXAUTH["APPS"][appid]["grant_type"]
            }
        )
        access_token_result = json.loads(response.text)
        return access_token_result

    def check_access_token(self, access_token, openid):
        response = requests.get(
            url=settings.WXAUTH['WX_CHECK_TOKEN_URL'],
            params={
                'access_token': access_token,
                'openid': openid
            }
        )
        check_result = json.loads(response.text)
        return check_result

    def refresh_access_token(self, appid, refresh_token):
        response = requests.get(
            url=settings.WXAUTH['WX_REFRESH_TOKEN_URL'],
            params={
                'appid': appid,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        refresh_token_result = json.loads(response.text)
        return refresh_token_result

    def get_user_info(self, access_token, openid):
        response = requests.get(
            url=settings.WXAUTH['WX_USERINFO_URL'],
            params={
                'access_token': access_token,
                'openid': openid
            }
        )
        user_info_result = json.loads(response.content.decode())
        return user_info_result
