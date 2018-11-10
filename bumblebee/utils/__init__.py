from .safecheck import safeCheck, slowDown
from .customuuid import genToken
from .pipeline import MongoDBPipeline
from .sigmaactions import sigmaActions
from .pinsheaders import pins_headers
from .sumchars import sumChars


class SelfAssemlingClass():
    def __init__(self, doc):
        self.__dict__ = doc
