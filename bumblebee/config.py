import redis


class ConfigError(Exception):

    def __init__(self, msg):
        print(msg)


class Headers():
    # TODO random header items & newest Chrome version
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 \
            Safari/537.36', }


class Bilibili(Headers):

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=2)

    # cookies_file = 'cookies/bilibili.json'
    cookies_domain = '.bilibili.com'
    member = 'https://member.bilibili.com/'
    default_dir = 'bilibee/cchan'

    preupload_params = {'os': 'bos',
                        'bucket': 'bvcupcdnbosxg',
                        'r': 'bos',
                        'profile': 'ugcupos/fetch',
                        'ssl': 0}

    def __init__(self, debug=True):

        if debug:
            self.cookies_file = 'cookies/bilitest.json'
        else:
            self.cookies_file = 'cookies/bilibili.json'

        self.headers = self.headers.copy()
        self.headers['referer'] = f'{self.member}video/upload.html'
        self.headers['x-requested-with'] = 'XMLHttpRequest'

        self.bce = {}
        self.bce['host'] = 'https://hk-2.bcebos.com'
        self.bce['bucket'] = 'bvcupcdnbosxg'
        self.bce['querystring'] = 'uploads'

        self.endpoints = {}
        self.endpoints['preupload'] = f'{self.member}/preupload'
        self.endpoints['pre_add'] = f'{self.member}/x/geetest/pre/add'
        self.endpoints['add'] = f'{self.member}/x/vu/web/add'
        self.endpoints['postPO'] = 'https://upos-hz-upcdnws.acgvideo.com/ugc/'


class CChan(Headers):

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=2)

    cookies_domain = '.cchan.tv'
    cookies_file = 'cookies/cchan.json'
    default_dir = 'bilibee/cchan'
    root = 'https://www.cchan.tv'

    good_cats = {
        'fashion',
        'nail',
        'make',
        'hair',
        'sweets',
    }

    def __init__(self):
        # weird...
        self.headers = self.headers.copy()

        self.endpoints = {}
        self.endpoints['ranking'] = f'{self.root}/ranking/'
        self.endpoints['watch'] = f'{self.root}/watch/'
        self.endpoints['video_file'] = 'https://ccs3.akamaized.net/cchanclips/'


class Instagram(Headers):

    # db not decided yet since this is on hold
    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=0)

    cookies_file = ''
    cookies_domain = ''
    root = ''


class Zhihu(Headers):

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=1)

    cookies_file = 'cookies/zhihu.json'
    cookies_domain = '.zhihu.com'
    root = 'https://www.zhihu.com'
    # get this by get self info
    # url_token = 'self_url_token'
    endpoints = {}

    def __init__(self):

        self.url_token = self._getSelfURLToken()

        # weird...
        self.headers = self.headers.copy()
        self.headers['referer'] = {
            'referer': f'{self.root}/people/{self.url_token}'}

        self.endpoints['postPins'] = f'{self.root}/api/v4/pins'
        self.endpoints['getFolloweeList'] = f'{self.root}/api/v4/members/\
                                       {self.url_token}/followees'
        self.endpoints['grabRecFeed'] = f'{self.root}/api/v3/feed/topstory\
                                        /recommend'

    # TODO

    def _getSelfURLToken(self):
        import requests
        return ''
