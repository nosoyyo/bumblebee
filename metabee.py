import utils
from bumblebee import BumbleBee
from config import self_url_token, root


class MetaBee():

    bee = BumbleBee('cookies.json')

    @utils.safeCheck
    def getFolloweeCount(self, url_token=self_url_token) -> int:
        endpoint = f'{root}/api/v4/members/{url_token}/followees'
        return self.bee._GET(endpoint)['paging']['totals']

    @utils.safeCheck
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
            result = self.bee._GET(endpoint)['data']
        elif type is 'all':
            result = self.bee._GETALL(endpoint)
        return [m['url_token'] for m in result]

    def actionsSince(self):
        '''
        number of actions since a given timenode.
        '''
        raise NotImplementedError
