# -*- coding: utf-8 -*-

"""Python sina weibo sdk.
Rely on `requests` to do the dirty work, so it's much simpler and cleaner
than the official SDK.
For more info, refer to:
http://lxyu.github.io/weibo/
"""
import json
import time
import requests
from urllib.parse import urlencode

from config import Weibo
from bees import AbstractBee


class WeiboBee():

    config = Weibo()
    endpoints = config.endpoints
    expires_at = ''
    s = requests.Session()
    s.headers = config.headers.copy()
    bee = AbstractBee(config, s)
    r = bee.r

    def __init__(self, token=None):

        # init basic info
        self.client_id = APP_KEY
        self.client_secret = APP_SECRET
        self.redirect_uri = ''
        self.s.auth = USERNAME, PASSWORD

        # activate client directly if given token
        if token:
            self.set_token(token)

    @property
    def authorize_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        return f"{self.endpoints['auth']}/{urlencode(params)}"

    @property
    def alive(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return False

    def set_code(self, authorization_code):
        """Activate client by authorization_code.
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        # break dev
        token = self.bee._POST(self.token_url, data=params)
        self._assert_error(token)

        token['expires_at'] = int(time.time()) + int(token.pop('expires_in'))
        self.set_token(token)

    def set_token(self, token):
        """Directly activate client by access_token.
        """
        self.token = token

        self.uid = token['uid']
        self.access_token = token['access_token']
        self.expires_at = token['expires_at']

        self.s.params = {'access_token': self.access_token}

    def _assert_error(self, d):
        """Assert if json response is error.
        """
        if 'error_code' in d and 'error' in d:
            raise RuntimeError("{0} {1}".format(
                d.get("error_code", ""), d.get("error", "")))

    def get(self, uri, **kwargs):
        """Request resource by get method.
        """
        url = f"{self.endpoints['api_url']}{uri}.json"

        # for username/password client auth
        if self.s.auth:
            kwargs['source'] = self.client_id

        res = json.loads(self.s.get(url, params=kwargs).text)
        self._assert_error(res)
        return res

    def post(self, uri, **kwargs):
        """Request resource by post method.
        """
        url = "{0}{1}.json".format(self.api_url, uri)

        # for username/password client auth
        if self.s.auth:
            kwargs['source'] = self.client_id

        if "pic" not in kwargs:
            res = json.loads(self.s.post(url, data=kwargs).text)
        else:
            files = {"pic": kwargs.pop("pic")}
            res = json.loads(self.s.post(url,
                                         data=kwargs,
                                         files=files).text)
        self._assert_error(res)
        return res


params = {}
params['act'] = 'post'
params['mid'] = 4306308818151564
params['uid'] = 6849774137
params['forward'] = 0
params['isroot'] = 0
params['content'] = '手工课上剪开的易拉罐'
params['location'] = 'v6_content_home'
params['module'] = 'scommlist'
params['group_source'] = 'group_all'
params['rid'] = 1_0_8_3071606790159465549_0_0
params['pdetail'] = ''
params['_t'] = 0
