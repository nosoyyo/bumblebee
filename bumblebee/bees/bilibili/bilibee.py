__doc__ = 'baidubce 2to3 by nosoyyo'
__version__ = 'baidubce for py3 ver 2c374'

import os
import json

from bees import AbstractBee
from config import Bilibili
from utils.baidubce.services.bos.bos_client import BosClient
from utils.baidubce.auth.bce_credentials import BceCredentials
from utils.baidubce.bce_client_configuration import BceClientConfiguration

'''
DEBUG STUFF
file = '/Users/nosoyyo/downloads/test.mp4'

AccessKeyId = "0e84cc78e32111e89487cd9f7fafef9f"
Expiration = "2018-11-08T18:39:35Z"
SecretAccessKey = "f8505e7ada80435daee2d5cfb7e0b5fc"
SessionToken = "MjUzZjQzNTY4OTE0NDRkNjg3N2E4YzJhZTc4YmU5ZDh8AAAAAFICAADsk6iYCf1SJeNajwUkr57prifDYpaiXmSacR9E3HAEtQ05Xe6qn8MD3quYBprPAstiIqA+noOnWIk8UzoueAdTLWXEOhO4SJCrHuXuL/nR46zk4bgx7dakVETkfAYwa+0MRoPnCeRbvDgjDxh+e/okFIJ5m/BX/0VbI5pKFDaznU4mP2ZR3evxZ2kuxv7NIW40w1FUwehBNlZ1lMBmZRVkbbEL8pvRtieczhtVlMkkEytKbFs0OiuDBQrCpTdeJGZ5rWA61JPvBpcY8p2W5Sh/jegr6nGIKzdz826YCDOxtJ6pXBrXmrKaHW3rppgcnw3fp1ydS+uBQfQ7EYtl77MkuC9LQxfp72l/44ejXvHLZAblpjwHByCzzEZ5p1GcvFSiHSNcVfPGDdmdt0Gd/FfWGAmf7RM5aHPuFU8sQzX1vuEE27zv5Bp6TxJpYV0sPcn4zeE0jJDkvmMiJ2X5xlAz"
bili_filename = "i181108bozdu9w84w4u2v34ug6zn9qtu"
key = "i181108bozdu9w84w4u2v34ug6zn9qtu.mp4"
biz_id = 62315505
bucket = "bvcupcdnbosxg"
endpoint = "hk-2.bcebos.com"
fetch_url = "//upos-hz-upcdnws.acgvideo.com/ugc/i181108bozdu9w84w4u2v34ug6zn9qtu.mp4?name=clip.mp4&fetch=&output=json&profile=ugcupos%2Ffetch&biz_id=62315505"
'''


class SelfAssemlingClass():
    def __init__(self, doc):
        self.__dict__ = doc


class PreuploadResp(SelfAssemlingClass):
    pass


class PutObjectResp(SelfAssemlingClass):
    pass


class BiliBee():

    config = Bilibili()
    bee = AbstractBee(config)
    bee.headers = config.headers.copy()
    preupload_params = config.preupload_params

    def checkVideos(self, path: str = None) -> list:
        '''
        check the default path, collect videos for uploading.

        : return: a `list` of video file path(s)
        '''
        _dir = path or self.config.default_dir
        return [f for f in os.listdir(_dir) if f.endswith('.mp4')]

    def upload(self, videos: list):
        '''
        : param videos: a `list` of video file_names
        '''
        for v in videos:
            self.middle = PreuploadResp(self.preUpload(v))
            self.upload_url = 'https:' + self.middle.fetch_url
            self.bee.headers.update(self.middle.fetch_headers)
            po_resp = self.putObject(v)
            po_result = PutObjectResp(json.loads(po_resp.text))
            self.postPO()

    def preUpload(self, file_name) -> json:
        '''
        Get AK/SK, fetch_headers etc.
        '''
        self.preupload_params['name'] = file_name
        full_name = self.config.default_dir + file_name
        self.preupload_params['size'] = os.path.getsize(full_name)
        return self.bee._GET(self.config.endpoints['preupload'],
                             _params=self.preupload_params)

    def detectSTSAuthExpire(self):
        '''
        check if time() is bigger than middle.Expiration
        '''
        pass

    def putObject(self):
        '''
        call baidubce put_object_from_file method.

        :return: resp of requests
        '''
        config = BceClientConfiguration(
            credentials=BceCredentials(
                access_key_id=self.middle.AccessKeyId,
                secret_access_key=self.middle.SecretAccessKey
            ),
            endpoint=self.middle.endpoint
        )
        bos_client = BosClient(config)
        resp = bos_client.put_object_from_file(
            self.middle.bucket,
            self.middle.key,
            self.preupload_params['name'],
        )
        return resp

    def postPO(self):
        h = self.bee.headers.copy()
        h.update(self.middle.fetch_headers)
        _params = {}
        _params['name'] = self.preupload_params['name']
        _params['fetch'] = None
        _params['output'] = 'json'
        _params['profile'] = 'ugcupos/fetch'
        _params['biz_id'] = self.middle.biz_id
        endpoint = self.endpoints['postPO'] + self.middle.key
        resp = self.bee._POST(endpoint, headers=h, _params=_params)
        return json.loads(resp.text)

    def preAdd(self):
        resp = self.bee._GET(self.pre_add)

    # 3
    csrf = 'bb1b31e6c8c70215d0d3f34e6beb32f6'
    add = Bilibili.member
    _add_params = {'csrf': csrf}

    some_title = '美丽的日本视频'
    desc = '一段发人深省的对话'
    middle = {'bili_filename': ''}

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
