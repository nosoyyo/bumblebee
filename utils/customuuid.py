from uuid import uuid4


def genToken(len: int = 32):
    if len is 32:
        return uuid4().__str__().replace('-', '')
    else:
        raise NotImplementedError
