import utils
from bumblebee import BumbleBee
from contentbee import ContentBee
from config import self_url_token, root


class ActionBee():

    bee = ContentBee()

    def poachThank(self, _id):
        '''
        '''
        def dealResp(text: str):
            if text == 'true':
                return True
            elif text == 'false':
                return False
            else:
                raise NotImplementedError

        endpoint = f'{root}/api/v4/answers/{_id}/thankers'
        resp = self.bee._GET(endpoint)
        return dealResp(resp['is_thanked'])

    @utils.safeCheck
    def someThanks(self):

        feed = self.bee.grabRecFeed()
        for f in feed:
            _id = f['id'].split('.')[0].split('_')[-1]
            self.poachThank(_id)
