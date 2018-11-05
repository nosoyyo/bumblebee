import time
from random import random

from config import Zhihu
from models.answer import Answer
from .contentbee import ContentBee


class WorkingBee(ContentBee):
    '''
    Daily routines.

    0. do some basicThanks
    '''

    def _GETALL(self, url: str) -> dict:
        resp = self._GET(url)
        if resp['paging']:
            count = resp['paging']['totals']
            print(f'totals: {count}')
        result = resp['data']
        while not resp['paging']['is_end']:
            offset = {'offset': int(resp['paging']['next'].split('=')[-1])}
            resp = self._GET(url, _params=offset)
            result += resp['data']
        return result

    def basicThanks(self, url_token=None):
        '''
        Grab answers from feed, thank them.

        # TODO: thank a certain person for several times.
        # NOTICE: `self.poachThank` only accept `Answer` obj.
        '''
        feed = self.grabRecFeed()
        thanked = 0
        for f in feed:
            if f['target']['type'] == 'answer':
                a = Answer(doc=f['target'])
                nap = random() * 10
                print(f'taking a {nap} secs nap...')
                time.sleep(nap)
                self.poachThank(a)
                thanked += 1
        print(f'{thanked} answers thanked.')

    def checkNotis(self):
        self.poachNotis()
        raise NotImplementedError

    def poachNotis(self) -> bool:
        raise NotImplementedError

    # TODO
    def postPins(self, text):
        endpoint = Zhihu.endpoints['postPins']
        content = [{"type": "text", "content": f'<p> {text} </p>'}]
        _data = {'content': content, 'version': 1, 'source_pin_id': 0}
        resp = self._POST(endpoint, data=_data)
        return resp
