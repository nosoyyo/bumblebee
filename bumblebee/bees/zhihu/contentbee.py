import time
import functools

import utils
from .bumblebee import BumbleBee
from config import Zhihu


class ContentBee(BumbleBee):

    z = Zhihu()
    root = z.root
    url_token = z.url_token

    def sessionTokenCheck(func):
        '''
        first fetch a session token from redis
        then check if it still living(life set to 2hrs for now)
        pass the token to the func if the token is living
        or gen a new token and write it into redis
        '''
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            current_token = self.r.hkeys('session_token')[0]
            if not current_token:
                current_token = utils.genToken()
                token_born = time.time()
                self.r.hset('session_token', current_token, token_born)
            else:
                token_born = float(self.r.hvals('session_token')[0])

            if time.time() - token_born >= 7200:
                self.r.hdel('session_token', current_token)
                current_token = utils.genToken()
                token_born = time.time()
                self.r.hset('session_token', current_token, token_born)
                print('token expired. generated a new one & saved in redis.')
            else:
                print('sessionTokenCheck passed. no problem.')

            return func(self, token=current_token, *args, **kw)
        return wrapper

    @utils.safeCheck
    @sessionTokenCheck
    def grabRecFeed(self, token: str = None, q=3) -> list:
        '''
        return a list of answer dicts.

        :param token: Session token. `session_token`
        :param q: nums of items per fetch (NotImplemented)
        '''
        endpoint = self.z.endpoints['grabRecFeed']
        _params = {'session_token': token, 'desktop': 'true', 'action': 'down'}
        resp = self._GET(endpoint, _params=_params)
        return resp['data']
