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
        '''
        feed = self.grabRecFeed()
        for f in feed:
            a = Answer(doc=f['target'])
            self.poachThank(a.id)
