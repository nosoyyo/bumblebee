import os
import time
import redis
from bs4 import BeautifulSoup

from config import CChan
from bees import AbstractBee
from utils import sumChars, fromTimeStamp


class CChanBee():

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=2)
    r = redis.Redis(connection_pool=cpool)

    config = CChan()
    bee = AbstractBee(config)

    def __init__(self):
        '''
        '''
        ranking = self.config.endpoints['ranking']
        resp = self.bee._GET(ranking)
        soup = BeautifulSoup(resp.text, 'lxml').select('div.box-general-list')

        soup = self.goodCatsFilter(soup)
        if self.grabInfo(soup):
            print(f'some info updated.')
        else:
            print('all info already have.')

        # get the raw URI of video pages
        self.top20 = [item.a['href'] for item in soup]
        self.top20 = [sumChars(i).replace('watch', '')
                      for i in self.top20]

        # cache the states into redis
        now = time.time()
        self.r.hset('ccb_init', now, self.top20)

        # see if any changes occured
        hkeys = self.r.hkeys('ccb_init')
        hkeys.sort()
        last_probe = hkeys[-2]
        if len(hkeys) >= 2:
            last_state = sumChars(self.r.hget('ccb_init', last_probe))
        else:
            last_state = ''
        this_state = sumChars(self.top20)
        change_flag = not bool(this_state == last_state)

        if change_flag:
            # grab stuff while in need
            flag = self.checkIfGrabbed()
            if flag:
                self.grab()
        else:
            since = fromTimeStamp(last_probe)
            print(f'nothing changed since {since[0]} {since[1]}')

    def grabInfo(self, soup):

        flag = False

        for item in soup:
            URI = sumChars(item.a['href']).replace('watch', '')
            source = self.r.hget('video_source', URI)
            title = self.r.hget('video_title', URI)
            desc = self.r.hget('video_desc', URI)

            if not source:
                source = f'https://www.cchan.tv/watch/{URI}'
                self.r.hset('video_source', URI, source)
                print(f'\n{URI} source {source} saved.')
                flag = True
            if not title:
                title = item.select('a.anchor-content-general-list')[0].text
                self.r.hset('video_title', URI, title)
                print(f'\n{URI} title {title} saved.')
                flag = True
            if not desc:
                endpoint = self.config.endpoints['watch'] + URI
                resp = self.bee._GET(endpoint)
                soup = BeautifulSoup(resp.text, 'lxml')
                desc = soup.select('div.auto-link')[0].text
                desc = desc.replace('\r', '\n')
                self.r.hset('video_desc', URI, desc)
                print(f'{URI} desc {desc} saved.\n')
                flag = True

        return flag

    def goodCatsFilter(self, soup):
        result = []
        chars = sumChars(self.config.good_cats)

        for item in soup:
            if item.select('a.mark-category')[0]['href'].split('/')[-2] in chars:
                result.append(item)
        print(f'{len(result)} items selected from soup.')
        return result

    def checkIfGrabbed(self) -> bool:
        '''
        check local storage and redis for repeated videos.

        :return: <bool> return False if nothing need to do.
        '''

        # deal with local storage
        cu = os.getlogin()
        self.full_path = f'/Users/{cu}/{self.config.default_dir}'
        try:
            os.listdir(self.full_path)
        except FileNotFoundError:
            os.makedirs(self.full_path)
        grabbed = [i.replace('.mp4', '') for i in os.listdir(self.full_path)]
        if '.DS_Store' in grabbed:
            grabbed.remove('.DS_Store')

        # deal with the fresh meat
        self.top20 = [x for x in self.top20 if x not in grabbed]
        print(f'\n{len(self.top20)} new items to grab.')

        return bool(len(self.top20))

    def grab(self):
        for URI in self.top20:
            print(f'downloading {URI}.mp4 ...')
            started = time.time()
            resp = self.bee._GET(
                f'https://ccs3.akamaized.net/cchanclips/{URI}/clip.mp4')
            usage = time.time() - started

            # local storage
            with open(f'{self.full_path}/{URI}.mp4', 'wb') as f:
                f.write(resp.content)

            # save title into redis

            # stats
            size = os.path.getsize(f'{self.full_path}/{URI}.mp4')
            print(f'{URI}.mp4 saved on disk.')
            print(f'{size} bytes, {usage:.1f} seconds. \n\
            {size / usage / 1024:.1f} kb/s')
