import json
from requests.structures import CaseInsensitiveDict


def loadIfJson(_input: str) -> bool:
    if isinstance(_input, bytes):
        _input = _input.decode()
    try:
        return json.loads(_input)
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
        elif isinstance(doc, CaseInsensitiveDict):
            self.__dict__ = dict(doc)
        else:
            print(
                'SelfAssemblingClass: only accept `dict` or something hasattr `__dict__`')
        self._recurse(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__.keys()

    def __repr__(self):
        return f'attrs: {[k for k in self.__dict__.keys()].__str__()}'

    def _recurse(self, _input):
        doc = None
        if isinstance(_input, dict) or loadIfJson(_input) or isinstance(_input, CaseInsensitiveDict):
            for k in _input.keys():
                if isinstance(_input[k], dict):
                    doc = _input[k].copy()
                elif loadIfJson(_input[k]):
                    doc = loadIfJson(_input[k]).copy()
                elif isinstance(_input, CaseInsensitiveDict):
                    doc = dict(doc).copy()

                if doc:
                    _input[k] = SelfAssemblingClass(doc)
                    self._recurse(_input[k])
