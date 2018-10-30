import json
import time
from random import random
import functools

# import jfw
import requests
from config import root, self_url_token, cookies_domain


class BumbleBeeError(Exception):
    pass


class BumbleBee():

    # print(jfw.__doc__)

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
        def wrapper(*args, **kw):
            slowness = random() + random() + random()
            time.sleep(slowness)
            print(f'idiot, slow down...{slowness:.2f}')
            return func(*args, **kw)
        return wrapper

    @slow_down
    def _GET(self, url: str, _params: dict = None) -> dict:
        '''
        :param _params: {'include':['a,b']}
        '''
        if _params is None:
            _params = {}
        resp = requests.get(url, cookies=self.cookies,
                            headers=self.headers, params=_params)
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

    def getFollowees(self,
                     url_token=self_url_token,
                     offset=0,
                     type='latest') -> list:
        '''
        :param url_token: <str> Only `url_token` works in url when fetching.
        :param offset: <int>
        '''
        endpoint = f'{root}/api/v4/members/{url_token}/followees'
        if type is 'latest':
            result = self._GET(endpoint)['data']
        elif type is 'all':
            result = self._GETALL(endpoint)
        return [m['url_token'] for m in result]

    def pins(self):
        return
