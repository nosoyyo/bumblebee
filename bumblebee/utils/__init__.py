from .bce.bce_v1_signer import sign
from .sumchars import sumChars
from .customuuid import genToken
from .pipeline import MongoDBPipeline
from .pinsheaders import pins_headers
from .sigmaactions import sigmaActions
from .safecheck import safeCheck, slowDown


class SelfAssemlingClass():
    def __init__(self, doc=None):
        if doc:
            self.__dict__ = doc
