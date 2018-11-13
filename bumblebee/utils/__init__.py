import json

from .bce.bce_v1_signer import sign
from .sumchars import sumChars
from .customuuid import genToken
from .pipeline import MongoDBPipeline
from .pinsheaders import pins_headers
from .sigmaactions import sigmaActions
from .safecheck import safeCheck, slowDown
from .fromtimestamp import fromTimeStamp


def is_json(_input: str) -> bool:
    if isinstance(_input, bytes):
        _input = _input.decode()
    try:
        json.loads(_input)
        return True
    except Exception:
        return False


class SelfAssemblingClass():
    '''
    recursively assemble everything up
    '''

    def __init__(self, doc=None):
        if isinstance(doc, dict):
            self.__dict__ = doc.copy()
        elif hasattr(doc, '__dict__'):
            self.__dict__ = doc.__dict__.copy()
        else:
            print('SelfAssemblingClass: only accept `dict` \
                or something hasattr `__dict__`')
        self._recurse(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__.keys()

    def __repr__(self):
        return f'attrs: {[k for k in self.__dict__.keys()].__str__()}'

    def _recurse(self, _dict):
        for k in _dict.keys():
            if isinstance(_dict[k], dict):
                _dict[k] = SelfAssemblingClass(_dict[k])
                self._recurse(_dict[k])
