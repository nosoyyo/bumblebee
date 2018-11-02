import json
import time
import redis

# import jfw
import utils
import requests
from exceptions import BumbleBeeError
from config import root, self_url_token, cookies_file, cookies_domain


class BumbleBee():

    # print(jfw.__doc__)

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=1)
    r = redis.Redis(connection_pool=cpool)

    def __init__(self):

        self.self_url_token = self_url_token

        with open(cookies_file) as f:
            cookies = json.load(f)
        self.cookies = {item['name']: item['value']
                        for item in cookies if item['domain']
                        == cookies_domain}
        # TODO
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 \
            Safari/537.36',
            'referer': f'{root}/people/{self_url_token}'}

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
            raise BumbleBeeError(101)
        else:
            try:
                result = json.loads(resp.text)
                print('1 result grabbed.')
                return result
            except json.JSONDecodeError:
                raise BumbleBeeError(102)

    def _GETALL(self, url: str) -> dict:
        resp = self._GET(url)
        if resp['paging']:
            count = resp['paging']['totals']
            print(f'totals: {count}')
        result = resp['data']
        while not resp['paging']['is_end']:
            offset = {'offset': int(resp['paging']['next'].split('=')[-1])}
            resp = self._GET(url, _params=offset)
            result += resp['data']
        return result

    @utils.slowDown
    def _POST(self, url: str, _params: dict = None) -> dict:
        '''
        :param _params: {'include':['a,b']}
        '''
        if _params is None:
            _params = {}

        try:
            resp = requests.post(url, cookies=self.cookies,
                                 headers=self.headers, params=_params)
        except Exception as e:
            raise BumbleBeeError(103)
        finally:
            utils.sigmaActions(self.r, time.time())

        try:
            result = json.loads(resp.text)
            print('1 result grabbed.')
            return result
        except json.JSONDecodeError:
            print('Cannot decode JSON for', url)
            raise BumbleBeeError(104)

    @utils.slowDown
    def _DELETE(self, url: str) -> str:
        raise NotImplementedError

    def getPersonDoc(self, url_token: str = None) -> dict:
        url_token = url_token or self_url_token
        return self._GET(f'{root}/api/v4/members/{url_token}')

    def poachThank(self, a) -> bool:
        '''
        Accepting only `Answer` object.
        '''
        endpoint = f'{root}/api/v4/answers/{a.id}/thankers'
        resp = self._POST(endpoint)
        print(f"thanked {a.author.name}'s answer on {a.question['title']}")
        sigma = self.r.hincrby('sigma_thanked', a.id)
        print(f'{a.author.name} has been thanked for {sigma} times.')
        return resp['is_thanked']

    # TODO
    def postPins(self, text):
        endpoint = f'{root}/api/v4/pins'
        content = [{"type": "text", "content": f'<p> {text} </p>'}]
        _data = {'content': content, 'version': 1, 'source_pin_id': 0}
        resp = self._POST(endpoint, data=_data)
        return resp
