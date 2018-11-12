from time import time
from datetime import datetime


def fromTimeStamp(timestamp: float = None, d=True, t=True) -> str:

    timestamp = timestamp or time()

    if not isinstance(timestamp, float):
        timestamp = float(timestamp)
    since = datetime.fromtimestamp(timestamp)
    _date = f'{since.year}.{since.month:02}.{since.day:02}'
    _time = f'{since.hour:02}:{since.minute:02}:{since.second:02}'

    if d and t:
        return _date, _time
    elif not t:
        return _date
    elif not d:
        return _time
