from .contentbee import ContentBee
from config import root


class WorkingBee(ContentBee):

    def someThanks(self):

        endpoint = f'{root}/api/v4/answers/{_id}/thankers'

        feed = self.grabRecFeed()
        for f in feed:
            _id = f['id'].split('.')[0].split('_')[-1]
            self.poachThank(_id)
