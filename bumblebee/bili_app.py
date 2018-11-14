'''Copyright 2018 Paul Carino

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

__author__ = 'nosoyyo'
__doc__ = 'bumblebee sample app'
__version__ = '2c37a'

import os
import time
import json
import schedule
from random import random
from datetime import datetime

from config import CChan
from bees import BiliAtomBee, CChanBee
from bees.bilibili import BiliVideoFile
from utils import fromTimeStamp, asciiBigSuccess

CCHAN_CONF = CChan()
WORKABLE = True
UPLOAD_INTERVAL = 60 * 60


def buildMinute(seed=0):
    seed = seed or 1
    mins = f'{int(seed*random()*random()*100):02}'
    if 0 < int(mins) < 59:
        return mins
    else:
        result = buildMinute(seed=random())
        if result:
            return result
        else:
            return '01'


MORNING0 = f'9:{buildMinute()}'
MORNING1 = f'11:{buildMinute()}'
AFTERNOON0 = f'17:{buildMinute()}'
AFTERNOON1 = f'19:{buildMinute()}'
EVENING0 = f'21:{buildMinute()}'
EVENING1 = f'23:{buildMinute()}'


def checkCChan():
    now = fromTimeStamp()
    print(f'\n----------\ncheckCChan wake up at {now}')
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


def checkLocalStorage(CCHAN_CONF, path: str = None) -> list:
    '''
    check the default path, collect videos for uploading.

    : return: a `list` of video file path(s)
    '''
    _dir = path or BiliVideoFile.full_path
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
    print(f'preparing upload under name of {BiliAtomBee._whoami()}')

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
    videos = checkLocalStorage(CCHAN_CONF)

    # 3
    for v in videos:
        URI = v.split('.')[0]
        if URI not in uploaded:
            vf = BiliVideoFile(v)
            bab = BiliAtomBee(vf)
            # upload one once
            flag = bab.process()
            if flag:
                r.rpush('upload_log', time.time())
                asciiBigSuccess()
                break
        if flag:
            break

        else:
            aid = r.hget('video_aid', URI)
            print(f'video file {v} already uploaded, aid {aid}')

    return flag


schedule.every().hour.do(checkCChan)
schedule.every().day.at(MORNING0).do(job)
schedule.every().day.at(MORNING1).do(job)
schedule.every().day.at(AFTERNOON0).do(job)
schedule.every().day.at(AFTERNOON1).do(job)
schedule.every().day.at(EVENING0).do(job)
schedule.every().day.at(EVENING1).do(job)


def main():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
