import json
import time
import redis
import functools
from random import random

# import jfw
import requests
from config import root, self_url_token, cookies_domain


class BumbleBeeError(Exception):
    pass


class BumbleBee():

    # print(jfw.__doc__)

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=1)
    r = redis.Redis(connection_pool=cpool)

    def __init__(self, cookies_file: str):

        self.self_url_token = self_url_token

        with open(cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == cookies_domain}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 \
            Safari/537.36',
            'referer': f'{root}/people/{self_url_token}/following'}

    def slow_down(func):
        '''
        Speed control.
        '''
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            slowness = random() + random() + random()
            time.sleep(slowness)
            print(f'idiot, slow down...{slowness:.2f}')
            return func(self, *args, **kw)
        return wrapper

    @slow_down
    def _GET(self, url: str, _params: dict = None) -> dict:
        '''
        :param _params: {'include':['a,b']}
        '''
        if _params is None:
            _params = {}

        try:
            attempt = time.time()
            resp = requests.get(url, cookies=self.cookies,
                                headers=self.headers, params=_params)
        except Exception as e:
            print(f'some {e} happens during _GET')
        finally:
            self.r.lpush('actions', attempt)
            # record last 9999 actions timenode
            if self.r.llen('actions') > 9999:
                self.r.ltrim('actions', 0, 9999)

        if resp.status_code != requests.codes.ok:
            print("Status code:", resp.status_code, "for", url)
            raise BumbleBeeError
        else:
            try:
                result = json.loads(resp.text)
                print('1 result grabbed.')
                return result
            except json.JSONDecodeError:
                print('Cannot decode JSON for', url)
                raise BumbleBeeError

    def _GETALL(self, url: str) -> dict:
        resp = self._GET(url)
        result = resp['data']
        while not resp['paging']['is_end']:
            offset = {'offset': int(resp['paging']['next'].split('=')[-1])}
            resp = self._GET(url, _params=offset)
            result += resp['data']
        return result

    def getPersonDoc(self, url_token: str = None) -> dict:
        url_token = url_token or self_url_token
        return self._GET(f'{root}/api/v4/members/{url_token}')

    def _POST(self, url: str) -> str:
        raise NotImplementedError

    def _DELETE(self, url: str) -> str:
        raise NotImplementedError

    def pins(self):
        return
