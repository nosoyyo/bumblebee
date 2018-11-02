import logging

from .base import BeeModel
from .person import Person
from .question import Question
from exceptions import BumbleBeeAnswerError


# init
logging.basicConfig(
    filename='var/log/answer.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class Answer(BeeModel):
    '''

    '''

    col = 'answers'
    key_objs = []

    def __init__(self, answer_id=None, doc=None):
        '''
        Must explicitly state 'doc=doc' when use.
        '''
        self.m = super(Answer, self).m
        if doc:
            self.__dict__ = doc
            self.author = Person(doc=doc['author'])
            self.question = Question(doc=doc['question'])
            self.aloha(self.id)
        elif answer_id:
            self.aloha(answer_id)
        else:
            raise BumbleBeeAnswerError(3001)

    def __repr__(self):
        return 'Answer'

    def aloha(self, answer_id):
        '''
        Accept only `answer_id` which is eventually `Answer.id`
        '''
        query = {'id': answer_id}
        has_stored = bool(self.m.ls(query, self.col))
        print(f'answer {answer_id} has been stored: {has_stored}')

        if not has_stored:
            if self.id:
                self.save()
                logging.info(f'answer {self.id} saved.')
            else:
                raise BumbleBeeAnswerError(3002)
        else:
            retrieval = self.load(answer_id)
            self.__dict__ = retrieval
            self.ObjectId = retrieval['_id']
            logging.info(f'answer {self.id} recalled.')
