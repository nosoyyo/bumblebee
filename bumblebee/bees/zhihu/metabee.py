import utils
from .bumblebee import BumbleBee
from config import self_url_token, root


class MetaBee(BumbleBee):

    @utils.safeCheck
    def getFolloweeCount(self, url_token=self_url_token) -> int:
        endpoint = f'{root}/api/v4/members/{url_token}/followees'
        return self._GET(endpoint)['paging']['totals']

    @utils.safeCheck
    def getFolloweeList(self,
                        url_token=self_url_token,
                        offset=0,
                        type='latest') -> list:
        '''
        :param url_token: <str> Only `url_token` works in url when fetching.
        :param offset: <int>
        '''
        endpoint = Zhihu.endpoints['getFolloweeList']
        if type is 'latest':
            resp = self._GET(endpoint)
            count = resp['paging']['totals']
            print(count)
            result = resp['data']
        elif type is 'all':
            result = self._GETALL(endpoint)
        return [m['url_token'] for m in result]

    def actionsSince(self):
        '''
        number of actions since a given timenode.
        '''
        raise NotImplementedError
