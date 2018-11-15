import os
import time
import redis
import requests

from conf.cchan import CChan
from bees import AbstractBee
from utils import sumChars, fromTimeStamp


class CChanBee():

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=2)
    r = redis.Redis(connection_pool=cpool)

    config = CChan()
    s = requests.Session()
    bee = AbstractBee(config, s)

    def __init__(self):
        '''
        '''
        ranking = self.config.endpoints['ranking']
        resp = self.bee._SOUP(ranking)
        if not resp:
            return 'something wrong while grabbing ranking.'
        else:
            soup = resp.select('div.box-general-list')

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
                endpoint = f"{self.config.endpoints['watch']}/{URI}"
                desc = self.bee._SOUP(endpoint).select('div.auto-link')[0].text
                if not desc:
                    desc = 'to be completed.'
                else:
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
        print(f'{len(self.top20)} new items to grab.\n----------\n')

        return bool(len(self.top20))

    def grab(self):
        for URI in self.top20:
            print(f'downloading {URI}.mp4 ...')
            file_name = f'{self.full_path}/{URI}.mp4'
            url = f'https://ccs3.akamaized.net/cchanclips/{URI}/clip.mp4'
            self.bee._DOWNLOAD(url, file_name)
