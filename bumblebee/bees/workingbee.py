from .contentbee import ContentBee
from config import root


class WorkingBee(ContentBee):

    def someThanks(self, url_token):

        feed = self.grabRecFeed()
        for f in feed:
            _id = f['id'].split('.')[0].split('_')[-1]
            self.poachThank(_id)
