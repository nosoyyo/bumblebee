import os
import json
import time
import redis
from bs4 import BeautifulSoup

import utils
from core.respadapter import GeneralResp
from bees.exceptions import BumbleBeeError


class AbstractBee():
    '''
    Gerenralized crawler.

    :method _SOUP: return BeautifulSoup(resp.text)
    :method _DOWNLOAD: return bytes or save file_name to local storage.
    '''

    def __init__(self, site_obj, _session):

        self.cpool = site_obj.cpool
        with open(site_obj.cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == site_obj.domain}
        self.headers = site_obj.headers
        self.r = redis.Redis(connection_pool=self.cpool)
        self.s = _session

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
        resp = None
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

        if 'file' in kwargs:
            return resp.content
        else:
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

    def _SOUP(self, url: str):
        resp = self._GET(url)
        if resp:
            return BeautifulSoup(resp._content.decode(), 'lxml')

    def _DOWNLOAD(self, url: str, file_name=None):
        '''
        use this method to download files
        '''
        started = time.time()
        resp = self._GET(url, file=True)
        if not file_name:
            return resp
        else:
            with open(file_name, 'wb') as f:
                f.write(resp)
            print(f'{file_name} downloaded from {url}')

            # stats
            usage = time.time() - started
            size = os.path.getsize(file_name)
            print(f'{size} bytes, {usage:.1f} seconds. \n\
{size / usage / 1024:.1f} kb/s')
