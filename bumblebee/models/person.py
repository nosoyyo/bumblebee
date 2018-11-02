import logging

from .base import BeeModel
from config import self_url_token


# init
logging.basicConfig(
    filename='var/log/person.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class Person(BeeModel):
    '''

    '''

    col = 'persons'
    key_objs = []

    def __init__(self, url_token=None, doc=None):
        self.m = super(Person, self).m
        if doc:
            self.__dict__ = doc
            self.has_doc = True
            self.aloha(self.url_token)
        else:
            self.url_token = url_token or self_url_token
            self.has_doc = False
            self.aloha(url_token)

    def __repr__(self):
        return 'Person'

    def aloha(self, url_token):
        query = {'url_token': self.url_token}
        has_stored = bool(self.m.ls(query, 'persons'))
        if self.has_doc:
            log_name = self.name
        else:
            log_name = url_token
        print(f'person {log_name} has been stored: {has_stored}')

        if has_stored and not self.has_doc:
            retrieval = self.load()
            self.__dict__ = retrieval
            self.ObjectId = retrieval['_id']
            logging.info(f'aloha! person {self.name} seen again.')
        elif has_stored and self.has_doc:
            # TODO: compare the online version and the stored version
            pass
        else:
            if self.has_doc:
                self.save()
            else:
                # TODO: grab person doc then save then log
                raise NotImplementedError
