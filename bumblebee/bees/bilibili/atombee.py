import json
import logging

from config import Bilibili
from bees import AbstractBee
from utils import SelfAssemlingClass
from utils.bce import BosClient, BceCredentials, BceClientConfiguration

logging.basicConfig(
    filename='var/log/signer.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class PreuploadResp(SelfAssemlingClass):
    pass


class PutObjectResp(SelfAssemlingClass):
    pass


class BiliAtomBee():

    config = Bilibili(debug=True)
    bee = AbstractBee(config)
    bee.headers = config.headers.copy()

    def __init__(self, file_obj):
        self.file = file_obj
        self.config.preupload_params['name'] = file_obj.name
        self.config.preupload_params['size'] = file_obj.size
        print(f'bab now load up {self.file.name}, ready to fire!')

    def preUpload(self) -> json:
        '''
        Get AK/SK, fetch_headers etc.
        '''

        return self.bee._XGET(self.config.endpoints['preupload'],
                              _params=self.config.preupload_params)

    def process(self):

        middle = PreuploadResp(self.preUpload())
        # debug
        self.middle = middle
        self.bee.headers.update(middle.fetch_headers)
        po_resp = self.putObject(middle)
        # po_result = PutObjectResp(json.loads(po_resp.text))
        # self.postPO(middle)
        '''
        check if time() is bigger than middle.Expiration
        '''
        pass

    def putObject(self, middle):
        '''
        call baidubce put_object_from_file method.

        : return: resp of requests
        '''
        bce_config = BceClientConfiguration(
            credentials=BceCredentials(
                access_key_id=middle.AccessKeyId,
                secret_access_key=middle.SecretAccessKey
            ),
            endpoint=middle.endpoint
        )
        bce_config.security_token = middle.SessionToken
        bos_client = BosClient(bce_config)
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
        endpoint = self.config.endpoints['postPO'] + middle.key
        resp = self.bee._POST(endpoint, headers=h, _params=_params)
        return json.loads(resp.text)

    def preAdd(self):

        endpoint = self.config.endpoints['pre_add']
        resp = self.bee._XGET(endpoint)

    def add(self, middle)->int:
        '''
        :return: aid

        :param :
        '''
        csrf = self.bee.cookies['bili_jct']
        endpoint = self.config.endpoints['add'] + f'?csrf={csrf}'
        content_type = {'Content-Type': 'application/json;charset=UTF-8'}
        self.bee.headers.update(content_type)

        # source = self.bee.r.hget('video_source', self.file.URI)
        title = self.bee.r.hget('video_titles', self.file.URI)
        desc = self.bee.r.hget('video_desc', self.file.URI)
        # TODO add some elegancy
        desc = desc['200']

        payload = {'copyright': 2,
                   'videos': [{'filename': middle.key.replace('.mp4', ''),
                               'title': self.file.URI,
                               'desc': ''}],
                   'no_reprint': 1,
                   'source': f"https://www.cchan.tv/watch/{self.file.URI}",
                   'tid': 157,
                   'cover': '',
                   'title': title,
                   'tag': '美妆',
                   'desc_format_id': 0,
                   'desc': desc,
                   'dynamic': '',
                   'subtitle': {'open': 0, 'lan': ''}}

        self.preAdd()
        resp = self.bee._POST(endpoint, _data=payload)
        return resp['data']['aid']
