import time
import functools
from random import random


def safeCheck(func):
    '''
    Global actions limit.
    '''
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        # check if the 100th action is within last 5 mins
        the_100th_action = self.bee.r.lindex('actions', 100)
        the_1kth_action = self.bee.r.lindex('actions', 1000)
        the_2kth_action = self.bee.r.lindex('actions', 2000)
        if self.bee.r.llen('actions') == 9999:
            the_10kth_action = self.bee.r.lindex('actions', -1)
        else:
            the_10kth_action = None

        if the_100th_action:
            if time.time() - the_100th_action <= 300:
                nap = random()*200
                info = f'reach the 5mins limit. \
                    gotta take a {nap} secs nap.'
        elif the_1kth_action:
            if time.time() - the_1kth_action <= 1800:
                nap = random()*999
                info = f'reach the 30mins limit. \
                    gotta take a {nap} secs nap.'
        elif the_2kth_action:
            if time.time() - the_2kth_action <= 3600:
                nap = random()*1989
                info = f'reach the 60mins limit. \
                    gotta take a {nap} secs nap.'
        elif the_10kth_action:
            if time.time() - the_10kth_action <= 86400:
                nap = random()*12306
                info = f'reach the 24hrs limit. \
                    gotta take a {nap} secs nap.'
        else:
            nap = None

        if nap:
            print(info)
            time.sleep(nap)
        else:
            print('safeCheck() passed. no problem. go on. \n')
            return func(self, *args, **kw)
    return wrapper
