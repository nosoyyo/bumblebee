import redis


DEBUG = False


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
    domain = '.bilibili.com'
    account = 'https://account.bilibili.com'
    member = 'https://member.bilibili.com'
    default_dir = 'bilibee/cchan'

    preupload_params = {'os': 'bos',
                        'bucket': 'bvcupcdnbosxg',
                        'r': 'bos',
                        'profile': 'ugcupos/fetch',
                        'ssl': 0}

    def __init__(self, debug=DEBUG):

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
        self.endpoints['user_info'] = f'{self.account}/home/userInfo'

        self.endpoints['preupload'] = f'{self.member}/preupload'
        self.endpoints['pre_add'] = f'{self.member}/x/geetest/pre/add'
        self.endpoints['add'] = f'{self.member}/x/vu/web/add'
        self.endpoints['postPO'] = 'https://upos-hz-upcdnws.acgvideo.com/ugc/'


class CChan(Headers):

    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=2)

    domain = '.cchan.tv'
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
    domain = ''
    root = ''


class Weibo(Headers):

    # db not decided yet since this is on hold
    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, db=3)

    cookies_file = 'cookies/weibo.json'
    domain = '.weibo.com'
    root = 'https://weibo.com'
    default_dir = 'bumblebee/weibo'

    def __init__(self):
        self.api_ver = 2
        self.endpoints = {}
        self.endpoints['api'] = 'https://api.weibo.com'
        self.endpoints['auth'] = f"{self.endpoints['api']}/oauth2/authorize"
        self.endpoints['token'] = f"{self.endpoints['api']}\
/{self.api_ver}/oauth2/access_token"
        self.endpoints['api_url'] = f"{self.endpoints['api']}\
/{self.api_ver}"
