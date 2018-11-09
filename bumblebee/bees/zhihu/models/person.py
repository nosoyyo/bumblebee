import logging

from .base import BeeModel
from config import Zhihu


# init
logging.basicConfig(
    filename='var/log/person.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class Person(BeeModel):
    '''

    '''
    root = Zhihu.root
    cookies_domain = Zhihu.cookies_domain

    col = 'persons'
    key_objs = []

    def __init__(self, url_token=None, doc=None):
        self.m = super(Person, self).m
        if doc:
            self.__dict__ = doc
            self.has_doc = True
            # not sure about the url_token keyname in doc
            self.aloha(doc['url_token'])
        else:
            self.url_token = url_token or self.getSelfUrlTokenFromCookies()
            self.has_doc = False
            self.aloha(url_token)

    def __repr__(self):
        return 'Person'

    def getSelfUrlTokenFromCookies(self):
        raise NotImplementedError

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

    def getPersonDoc(self, url_token: str = None) -> dict:
        url_token = url_token or self.self_url_token
        return self._GET(f'{self.root}/api/v4/members/{url_token}')
