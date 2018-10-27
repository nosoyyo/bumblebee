import redis
from bumblebee import BumbleBee


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

    def __init__(self, url_token):
        '''
        '''
        # get all followees when init
        self.token = url_token
        print(f'check if {self.token} already existed in redis...')
        if not self.r.llen(f'{self.token}_followees'):
            print(f'{self.token} not exists. start grabbing followees...')
            self.followees = self.bee.getFollowees(
                url_token=self.token, type='all')
            for f in self.followees:
                self.pipe.lpush(f'{self.token}_followees', f)
            self.pipe.execute()
