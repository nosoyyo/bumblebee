import logging

from base import BeeModel
from bumblebee import bumblebee
from config import self_url_token


# init
logging.basicConfig(
    filename='var/log/user.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class Person(BeeModel):
    '''

    '''

    bee = BumbleBee('cookies.json')
    col = 'persons'
    key_objs = []

    def __init__(self, url_token=None):
        self.m = super(Person, self).m
        self.url_token = url_token or self_url_token
        self.aloha(url_token)

    def __repr__(self):
        return 'Person'

    def aloha(self, url_token):
        query = {'url_token': self.url_token}
        is_new = not bool(self.m.ls(query, 'persons'))
        print(f'is new: {is_new}')

        if is_new:
            doc = self.bee.getPersonDoc(url_token)
            self.__dict__ = doc

            self.save(self.id)
            logging.info(f'new user {self.name} saved.')
        else:
            retrieval = self.load(self.id)
            self.__dict__ = retrieval
            self.ObjectId = retrieval['_id']
            logging.info('aloha! user {} seen again.'.format(self.tele_id))
