import json
import time
import redis
import requests

import utils
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
    def _GET(self, url: str, _params: dict = None) -> dict:
        '''
        :param _params: {'include':['a,b']}
        '''
        if _params is None:
            _params = {}

        try:
            occur = time.time()
            resp = self.s.get(url, cookies=self.cookies,
                              headers=self.headers, params=_params)
        except Exception as e:
            print(f'some {e} happens during _GET')
        finally:
            utils.sigmaActions(self.r, occur)

        return resp

    @utils.slowDown
    def _XGET(self, url: str, _params: dict = None) -> dict:
        '''
        :param _params: {'include':['a,b']}
        '''

        resp = self._GET(url, _params=_params)

        try:
            result = json.loads(resp.text)
            print(f'stuff grabbed from {url}.')
            return result
        except json.JSONDecodeError:
            raise BumbleBeeError(1002)

    @utils.slowDown
    def _POST(self, url: str, headers=None, _data=None):
        '''
        :return ?: may return a `dict` or an `int` as http code

        :param _data: <dict> the data that requests.post needs.
        '''

        headers = headers or self.headers

        if _data is None:
            _data = {}

        try:
            resp = self.s.post(url, cookies=self.cookies,
                               headers=headers, json=_data)
        except Exception:
            raise BumbleBeeError(1003)
        finally:
            utils.sigmaActions(self.r, time.time())

        if resp.status_code == 200:
            try:
                result = json.loads(resp.text)
                print(f'stuff posted to {url}')
                return result
            except json.JSONDecodeError:
                print('Cannot decode JSON for', url)
                raise BumbleBeeError(1004)
        elif resp.status_code == 204:
            return 204
        else:
            return resp

    @utils.slowDown
    def _DELETE(self, url: str) -> str:
        raise NotImplementedError

    @utils.slowDown
    def _PUT(self, url: str) -> str:
        raise NotImplementedError
