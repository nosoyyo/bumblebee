import json
import time
import functools

import requests
from config import root, larva_url_token, cookies_domain

bee = BumbleBee('cookies.json')
slowness = 0.3


class BumbleBeeError(Exception):
    pass


class BumbleBee():

    def __init__(self, cookies_file: str):

        self.larva_url_token = larva_url_token

        with open(cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == cookies_domain}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 \
            Safari/537.36',
            'referer': f'{root}/people/{larva_url_token}/following'}

    def slow_down(func):
        '''
        Speed control.
        '''
        @functools.wraps(func)
        def wrapper(*args, **kw):
            time.sleep(slowness)
            print('idiot, slow down...')
            return func(*args, **kw)
        return wrapper

    @slow_down
    def _GET(self, url: str, _params: dict=None, all=False) -> dict:
        """
            _params: {'include':['a,b']}
        """
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
                return result
            except json.JSONDecodeError:
                print('Cannot decode JSON for', url)
                raise BumbleBeeError

    def getFollowees(self,
                     url_token=larva_url_token,
                     offset=0,) -> list:
        '''
        :param url_token: <str> Only `url_token` works in url when fetching.
        :param offset: <int>
        '''
        _params = {'offset': offset}
        resp = self._GET(
            f'{root}/api/v4/members/{url_token}/followees', _params)
        return [m['url_token'] for m in resp['data']]

    def pins(self):
        return
