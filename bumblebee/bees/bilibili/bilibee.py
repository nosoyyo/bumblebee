import os
import json
import requests

from .bumblebee import BumbleBee
from config import Bilibili

# 0

b = Bilibili()


def checkVideos(path: str) -> str:
    '''
    Read the path in config to realize videos for uploading.

    :return: video filename(s)
    '''
    pass


b.preupload_params['name'] = checkVideos(b.video_path)
b.preupload_params['size'] = os.path.getsize(b.preupload_params['name'])

bee = BumbleBee(b)


def preupload(bee: BumbleBee) -> json:
    resp = bee._GET(b.endpoints['preupload'],
                    params=bee.preupload_params)
    return json.loads(resp.text)


def upload(bee):
    middle = preupload(bee)

    # assert `middle` looks like this:
    middle = {'AccessKeyId': '7d01c687e0b911e8a92d1fef40f45d5d',
              'SecretAccessKey': '9309d87e300e400da1b4a4c2beae4b12',
              'SessionToken': 'MjUzZjQzNTY4OTE0NDRkNjg3N2E4YzJhZTc4YmU5ZDh8AAAAAFICAADsk6iYCf1SJeNajwUkr57pKffXQ1HuoR1/vVX6WDwyaoQBVScm5LdBzbcdv4MDCHsetcemuNiSlvPKeNncnRzrrZ7yIlpx/ZeegqNcfX+mlJdYDD0K/sPt96P1OyDz0zkw5Wxm2tjN7MtnV8NV51AwOG2RomMPcS4vT75Rtkn8liJeR4wYNXpLXyySluRBwIQtdxsKi9Z7WxTVwuSkVZcxy3X9XtDG5D9T8I4y9rGb6BJ4Hfn1fXTMo73W7Qmg83luSS0DsalDtwM0hw7MuXfcB0NNIuv6zWGh5TefOVL743b677nlroLpwAxjvPPWkpSMGjWpxL01UQLs5lHaUmDsPhhaqJdfQGD4LspOi6H8XgPl6KR1n/Nn50cap50qdqojB7RcsNub5PisEexj7XijZKuY2vAy9vwP6VxTr6uPJYhMPTT7UdSeJvvoGTWvOMQ5p7lQVWvmDktfbgsUxY3T',
              'Expiration': '2018-11-05T17:13:10Z',
              'bili_filename': 'i181105bo2ebmiz7doqjoc34sjpze0o3',
              'biz_id': 61960174,
              'bucket': 'bvcupcdnbosxg',
              'endpoint': 'hk-2.bcebos.com',
              'key': 'i181105bo2ebmiz7doqjoc34sjpze0o3.mp4',
              'fetch_url': '//upos-hz-upcdnws.acgvideo.com/ugc/i181105bo2ebmiz7doqjoc34sjpze0o3.mp4?name=clip.mp4&fetch=&output=json&profile=ugcupos%2Ffetch&biz_id=61960174',
              'fetch_headers': {'X-Upos-Fetch-Source': 'http://14.215.190.14/bvcupcdnbosxg/i181105bo2ebmiz7doqjoc34sjpze0o3.mp4',
                                'X-Upos-Auth': 'os=bos&cdn=bvcupcdnbosxg&access_id=1494471752&timestamp=1541394790&sign=ea68bafe2f154c9a4b893126ccc76d6f'},
              'OK': 1}


# 1
    bee.upload_url = 'https:' + middle['fetch_url']
    bee.headers.update(middle['fetch_headers'])
    resp = bee.post(bee.upload_url)
    return json.loads(resp.text)


# 2
def preAdd(bee):
    resp = bee._GET(bee.pre_add)


# 3
csrf = 'bb1b31e6c8c70215d0d3f34e6beb32f6'
add = 'https://member.bilibili.com/x/vu/web/add'
_add_params = {'csrf': csrf}

some_title = '美丽的日本视频'
desc = '一段发人深省的对话'

payload = {'copyright': 1,
           'videos': [{'filename': middle['bili_filename'],
                       'title': some_title,
                       'desc': desc}],
           'no_reprint': 1,
           'tid': 21,
           'cover': '',
           'title': 'test',
           'tag': '日常',
           'desc_format_id': 0,
           'desc': desc,
           'dynamic': '',
           'subtitle': {'open': 0, 'lan': ''}}
