import utils

from config import Zhihu


class MetaBee():

    def __init__(self):
        self.headers = self.headers.copy()
        self.headers['referer'] = {
            'referer': f'{self.root}/people/{self.url_token}'}

        self.endpoints['postPins'] = f'{self.root}/api/v4/pins'
        self.endpoints['getFolloweeList'] = f'{self.root}/api/v4/members/\
                                       {self.url_token}/followees'
        self.endpoints['grabRecFeed'] = f'{self.root}/api/v3/feed/topstory\
                                        /recommend'

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
