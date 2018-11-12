import os
import time
import json
import schedule
from datetime import datetime

from config import CChan
from utils import fromTimeStamp
from bees.bilibili import VideoFile
from bees import BiliAtomBee, CChanBee

cchan_config = CChan()
WORKABLE = True
INTERVAL = 60 * 60 * 6


def checkCChan():
    CChanBee()


def checkIfWorkable():
    '''
    check WORKABLE and INTERVAL
    '''
    flag = False
    global WORKABLE, INTERVAL
    now = datetime.now()
    if 2 < now.hour < 9:
        WORKABLE = False
        flag = False
    else:
        if:
            pass


def getAllUploadedVideos(r):

    result = []
    fetch = r.hvals('video_upload')
    for val in fetch:
        item = json.loads(val.replace("'", '"'))
        result.append([k for k in item.keys()][0])

    return result


def checkLocalStorage(cchan_config, path: str = None) -> list:
    '''
    check the default path, collect videos for uploading.

    : return: a `list` of video file path(s)
    '''
    _dir = path or VideoFile.full_path
    return [f for f in os.listdir(_dir) if f.endswith('.mp4')]


def checkUploadStatus():
    '''
    plan is to do upload every 6~8 hrs.
    so here we check if the interval is big enough.
    and if <now> is `workable` time
    '''


def main():
    '''
    processes:

    0. CChanBee() check for new stuff & download
    1. get all uploaded videos for
    2. check local storage
    3. bab.process() each vf in videos

    '''

    r = CChanBee.r
    r.hset('bili_app_log', time.time())

    # 0
    CChanBee()

    # 1
    uploaded = getAllUploadedVideos(CChanBee.r)

    # 2
    videos = checkLocalStorage(cchan_config)

    # 3
    for vf in videos:
        URI = vf.split('.')[0]
        if URI not in uploaded:
            bab = BiliAtomBee(vf)
            bab.process()
        else:
            aid = r.hget('video_upload', URI)
            print(f'video file {vf} already uploaded, aid {aid}')


schedule.every().hour.do(checkCChan)
schedule.every(3).hours.do(main)
