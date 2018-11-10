import os
import json

from config import Bilibili
from bees import AbstractBee
from utils import SelfAssemlingClass
from baidubce.services.bos.bos_client import BosClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration


class PreuploadResp(SelfAssemlingClass):
    pass


class PutObjectResp(SelfAssemlingClass):
    pass


class BiliAtomBee():

    config = Bilibili()
    bee = AbstractBee(config)
    bee.headers = config.headers.copy()

    def __init__(self, file_obj):
        self.file = file_obj
        self.config.preupload_params['name'] = file_obj.name
        self.config.preupload_params['size'] = file_obj.size

    def preUpload(self) -> json:
        '''
        Get AK/SK, fetch_headers etc.
        '''

        return self.bee._XGET(self.config.endpoints['preupload'],
                              _params=self.preupload_params)

    def upload(self):

        middle = PreuploadResp(self.preUpload())
        # debug
        self.middle = middle
        self.bee.headers.update(middle.fetch_headers)
        po_resp = self.putObject(middle)
        po_result = PutObjectResp(json.loads(po_resp.text))
        self.postPO(middle)

    def detectSTSAuthExpire(self):
        '''
        check if time() is bigger than middle.Expiration
        '''
        pass

    def putObject(self, middle):
        '''
        call baidubce put_object_from_file method.

        : return: resp of requests
        '''
        config = BceClientConfiguration(
            credentials=BceCredentials(
                access_key_id=middle.AccessKeyId,
                secret_access_key=middle.SecretAccessKey
            ),
            endpoint=middle.endpoint
        )
        bos_client = BosClient(config)
        resp = bos_client.put_object_from_file(
            middle.bucket,
            middle.key,
            self.file.full_name,
        )
        return resp

    def postPO(self, middle):
        h = self.bee.headers.copy()
        h.update(middle.fetch_headers)
        _params = {}
        _params['name'] = self.file.name
        _params['fetch'] = None
        _params['output'] = 'json'
        _params['profile'] = 'ugcupos/fetch'
        _params['biz_id'] = middle.biz_id
        endpoint = self.endpoints['postPO'] + middle.key
        resp = self.bee._POST(endpoint, headers=h, _params=_params)
        return json.loads(resp.text)

    def preAdd(self):
        resp = self.bee._XGET(self.pre_add)

    def add(self, middle, po_result):
        '''
        '''
        csrf = 'bb1b31e6c8c70215d0d3f34e6beb32f6'
        add_url = Bilibili.member
        add_params = {'csrf': csrf}

        some_title = self.bee.r.hget(
            'video_titles', self.URI)
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
