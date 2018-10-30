import time
import functools

import utils
from bumblebee import BumbleBee
from config import self_url_token, root


class ContentBee():

    bee = BumbleBee('cookies.json')

    def sessionTokenCheck(func):
        '''
        first fetch a session token from redis
        then check if it still living(life set to 2hrs for now)
        pass the token to the func if the token is living
        or gen a new token and write it into redis
        '''
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if not self.bee.r.hkeys('session_token'):
                current_token = utils.genToken()
                token_born = time.time()
                self.bee.r.hset('session_token', current_token, token_born)

            if time.time() - token_born >= 7200:
                current_token = utils.genToken()
                token_born = time.time()
                self.bee.r.hset('session_token', current_token, token_born)
                print('token expired. generated a new one and saved in redis.')
            else:
                print('sessionTokenCheck passed. no problem. \n')

            return func(self, token=current_token, *args, **kw)
        return wrapper

    @utils.safeCheck
    @sessionTokenCheck
    def grabRecFeed(self, token: str = None, q=3) -> list:
        '''
        return a list of answer dicts.

        :param token: Session token. `session_token`
        '''
        endpoint = f'{root}/api/v3/feed/topstory/recommend'
        _params = {'session_token': token, 'desktop': 'true', 'action': 'down'}
        resp = self.bee._GET(endpoint, _params=_params)
        return resp['data']
