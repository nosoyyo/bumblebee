import logging

from .base import BeeModel
from .person import Person
from exceptions import BumbleBeeQuestionError

# TODO at all

# init
logging.basicConfig(
    filename='var/log/question.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class Question(BeeModel):
    '''

    '''

    col = 'questions'
    key_objs = []

    def __init__(self, question_id=None, doc=None):
        '''
        Must explicitly state 'doc=doc' when use.
        '''
        self.m = super(Question, self).m
        if doc:
            self.__dict__ = doc
            if isinstance(doc['author'], dict):
                self.author = Person(doc=doc['author'])
            else:
                self.author = Person(doc=doc['author'].__dict__)
            self.has_doc = True
            self.aloha(self.id)
        elif question_id:
            self.has_doc = False
            self.aloha(question_id)
        else:
            raise BumbleBeeQuestionError(201)

    def __repr__(self):
        return 'Question'

    def aloha(self, question_id):
        '''
        Accept only `question_id` which is eventually `Question.id`
        '''
        query = {'id': question_id}
        has_stored = bool(self.m.ls(query, self.col))
        print(f'question has been stored: {has_stored}')

        if has_stored and not self.has_doc:
            retrieval = self.load()
            self.__dict__ = retrieval
            self.ObjectId = retrieval['_id']
            logging.info(f'aloha! question {self.title} reached again.')
        elif has_stored and self.has_doc:
            # TODO: compare the online version and the stored version
            pass
        else:
            if self.has_doc:
                self.save()
            else:
                # TODO: grab question doc and save and log
                pass
