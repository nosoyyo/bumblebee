import redis

from bumblebee import BumbleBee
from config import self_url_token


class Larva():
    '''
    :attr followees:
    :attr followers:
    '''
    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=1)
    r = redis.Redis(connection_pool=cpool)
    pipe = r.pipeline(transaction=False)
    bee = BumbleBee('cookies.json')

    def __init__(self, url_token: str=self_url_token):
        '''
        :param url_token:

        '''

        self.token = url_token

        # check or get followees when init
        print(f'check if {self.token} already existed in redis...')
        if not self.r.llen(f'{self.token}_followees'):
            print(f'{self.token} not exists. start grabbing followees...')
            self.followees = self.bee.getFollowees(
                url_token=self.token, type='all')
            print(f'{len(self.followees)} grabbed.')

            # sync into redis
            try:
                for f in self.followees:
                    self.pipe.lpush(f'{self.token}_followees', f)
                self.pipe.execute()
                print('synced into redis.')
            except Exception as e:
                print(e)
        else:
            print(f'{self.token} already existed. fetching from redis...')
            self.followees = self.r.lrange(f'{self.token}_followees', 0, -1)
            print(f'{len(self.followees)} fetched.')
