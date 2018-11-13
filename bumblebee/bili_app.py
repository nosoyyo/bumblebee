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
UPLOAD_INTERVAL = 60 * 60 * 6


def checkCChan():
    now = fromTimeStamp()
    print(f'checkCChan wake up at {now}')
    CChanBee()


def checkIfWorkable():
    '''
    check WORKABLE
    '''
    flag = False
    global WORKABLE
    now = datetime.now()
    if 0 < now.hour < 8:
        WORKABLE = False
        flag = False
    else:
        flag = True
    return flag


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


def job():
    '''
    processes:

    -1. check if workable
    0. CChanBee() check for new stuff & download
    1. get all uploaded videos for
    2. check local storage
    3. bab.process() each vf in videos

    '''

    flag = False
    now = fromTimeStamp()
    print(f'main job wake up at {now}')
    resp = BiliAtomBee.bee._XGET('https://account.bilibili.com/home/userInfo')
    if 'data' in resp:
        uname = resp['data']['uname']
        print(f'preparing upload under name of {uname}')

    # -1
    if not checkIfWorkable():
        print(f'{fromTimeStamp()} is not a workable time!')
        return False

    r = CChanBee.r

    # 0
    CChanBee()

    # 1
    uploaded = getAllUploadedVideos(CChanBee.r)

    # 2
    videos = checkLocalStorage(cchan_config)

    # 3
    for v in videos:
        URI = v.split('.')[0]
        if URI not in uploaded:
            vf = VideoFile(v)
            bab = BiliAtomBee(vf)
            # upload one once
            if bab.process():
                r.rpush('upload_log', time.time())
                break
        else:
            aid = r.hget('video_aid', URI)
            print(f'video file {v} already uploaded, aid {aid}')

    return flag


schedule.every().hour.do(checkCChan)
schedule.every(5).hours.do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
