import time
from random import random

from models.answer import Answer
from .contentbee import ContentBee


class WorkingBee(ContentBee):
    '''
    Daily routines.

    0. do some basicThanks
    '''

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
                time.sleep(nap)
                self.poachThank(a)
                thanked += 1
        print(f'{thanked} answers thanked.')
