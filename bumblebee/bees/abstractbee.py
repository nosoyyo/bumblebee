import json
import time
import redis
import requests

import utils
from core.respadapter import GeneralResp
from bees.exceptions import BumbleBeeError


class AbstractBee():
    '''
    Gerenralized crawler.
    '''
    s = requests.Session()

    def __init__(self, site_obj):

        self.cpool = site_obj.cpool
        self.r = redis.Redis(connection_pool=self.cpool)
        with open(site_obj.cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == site_obj.cookies_domain}
        self.headers = site_obj.headers

    # TODO
    def detectCookiesExpire(self):
        pass

    @utils.slowDown
    def _GET(self,
             url: str,
             headers=None,
             _params: dict = None,
             **kwargs) -> dict:
        '''
        :param _params: <dict>
        '''

        headers = headers or self.headers.copy()
        _params = _params or {}

        try:
            occur = time.time()
            resp = self.s.get(url, cookies=self.cookies,
                              headers=headers, params=_params)
        except Exception as e:
            print(f'some {e} happens during _GET')
        finally:
            utils.sigmaActions(self.r, occur)

        return GeneralResp(resp)

    @utils.slowDown
    def _XGET(self, url: str, _params: dict = None, **kwargs) -> dict:
        '''
        :param _params: <dict>
        '''
        if 'headers' in kwargs:
            headers = kwargs['headers']
        else:
            headers = self.headers.copy()
        accept = {'Accept': 'application/json, text/plain, */*'}
        headers.update(accept)
        resp = self._GET(url, _params=_params, headers=headers)

        return GeneralResp(resp)

    @utils.slowDown
    def _POST(self, url: str, headers=None, _data=None, _params=None):
        '''
        :return ?: may return a `dict` or an `int` as http code

        :param _data: <dict> the data that requests.post needs.
        '''

        headers = headers or self.headers.copy()

        content_type = {'Content-Type': 'application/json;charset=UTF-8'}
        headers.update(content_type)
        print(f"Content-Type: {headers['Content-Type']}")

        _data = _data or {}
        _params = _params or {}

        try:
            resp = self.s.post(url, cookies=self.cookies,
                               headers=headers, json=_data)
            return GeneralResp(resp)
        except Exception:
            raise BumbleBeeError()
        finally:
            utils.sigmaActions(self.r, time.time())

    @utils.slowDown
    def _DELETE(self, url: str) -> str:
        raise NotImplementedError

    @utils.slowDown
    def _PUT(self, url: str) -> str:
        raise NotImplementedError
