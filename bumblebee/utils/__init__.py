from .baidubceutils import *
from .sumchars import sumChars
from .customuuid import genToken
from .pipeline import MongoDBPipeline
from .pinsheaders import pins_headers
from .sigmaactions import sigmaActions
from .safecheck import safeCheck, slowDown


class SelfAssemlingClass():
    def __init__(self, doc):
        self.__dict__ = doc
