import json
import time
import redis

import utils
import requests
from exceptions import BumbleBeeError


class BumbleBee():
    '''
    Gerenralized crawler.
    '''

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=1)
    r = redis.Redis(connection_pool=cpool)

    def __init__(self, site_obj):

        with open(site_obj.cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == site_obj.cookies_domain}

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
            resp = requests.get(url, cookies=self.cookies,
                                headers=self.headers, params=_params)
        except Exception as e:
            print(f'some {e} happens during _GET')
        finally:
            utils.sigmaActions(self.r, occur)

        if resp.status_code != requests.codes.ok:
            raise BumbleBeeError(1001)
        else:
            try:
                result = json.loads(resp.text)
                print(f'stuff grabbed from {url}.')
                return result
            except json.JSONDecodeError:
                raise BumbleBeeError(1002)

    @utils.slowDown
    def _POST(self, url: str, _params: dict = None):
        '''
        :return ?: may return a `dict` or an `int` as http code
        :param _params: {'include':['a,b']}
        '''
        if _params is None:
            _params = {}

        try:
            resp = requests.post(url, cookies=self.cookies,
                                 headers=self.headers, params=_params)
        except Exception as e:
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

    @utils.slowDown
    def _DELETE(self, url: str) -> str:
        raise NotImplementedError

    @utils.slowDown
    def _PUT(self, url: str) -> str:
        raise NotImplementedError
