import json
import logging
import requests

from config import Bilibili
from bees import AbstractBee
from utils import SelfAssemblingClass, fromTimeStamp
from utils.bce import BosClient, BceCredentials, BceClientConfiguration

logging.basicConfig(
    filename='var/log/signer.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] \
    %(levelname)s %(message)s')


class AtomBeeError(Exception):
    pass


class PreuploadResp(SelfAssemblingClass):
    pass


class PutObjectResp(SelfAssemblingClass):
    pass


class BiliAtomBee():
    '''
    self.process() is the only method exposed.
    '''

    config = Bilibili()
    bee = AbstractBee(config)
    bee.headers = config.headers.copy()
    r = bee.r

    def __init__(self, file_obj):
        self.file = file_obj
        self.config.preupload_params['name'] = file_obj.name
        self.config.preupload_params['size'] = file_obj.size
        print(f'bab now load up {self.file.name}, ready to fire!')

    def _whoami(self):
        endpoint = self.config.endpoints['user_info']
        uname = self.bee._XGET(endpoint)

    def process(self)->bool:

        flag = False

        middle = PreuploadResp(self.preUpload())
        # debug
        self.middle = middle
        self.bee.headers.update(middle.fetch_headers)

        po_resp = self.putObject(middle)
        checkKeys = po_resp.metadata.__dict__.keys()
        if len(checkKeys) == 10:
            print(f'po_resp seems ok.')
        else:
            print(
                f'WARNING: po_resp got {checkKeys}, \
                putObject may have trouble.')

        # self.postPO(middle)
        # check if time() is bigger than middle.Expiration

        aid = self.add(middle)
        if aid:
            # simple check
            if isinstance(aid, int) and len(aid) == 8:
                is_aid_ok = True
            else:
                print(f'WARNING! aid {aid} is questionable!')
                flag = False

            if is_aid_ok:
                now = fromTimeStamp()
                self.r.hset('video_upload', now, {self.file.URI: aid})
                self.r.hset('video_aid', self.file.URI, aid)
                print(f'{self.file.URI} succesfully uploaded at {now}.')
                print(f'aid: {aid}')
                flag = True
        else:
            print(f'failed getting aid.')
            flag = False
        return flag

    def preUpload(self) -> json:
        '''
        Get AK/SK, fetch_headers etc.
        '''

        return self.bee._XGET(self.config.endpoints['preupload'],
                              _params=self.config.preupload_params)

    def putObject(self, middle):
        '''
        call baidubce put_object_from_file method.

        : return: resp of requests
        '''
        print(f'sending {self.file.name} upward...')

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
        print('putObject seems ok. starting further check....')

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
        return self.bee._POST(endpoint, headers=h, _params=_params)

    def preAdd(self) -> bool:

        endpoint = self.config.endpoints['pre_add']
        # TODO need to check if this is necessary
        resp = self.bee._XGET(endpoint)

        try:
            if resp['code'] == 0:
                print('preAdd seems ok.')
                return True
            else:
                print('Warning! preAdd seems in trouble.')
                return False
        except Exception:
            return False

    def buildPayload(self, middle):

        source = self.bee.r.hget('video_source', self.file.URI)
        title = self.bee.r.hget('video_title', self.file.URI)
        desc = self.bee.r.hget('video_desc', self.file.URI)
        # TODO add some elegancy
        if desc:
            desc = desc[:200]

        payload = {}
        if source:
            payload['source'] = source
        else:
            raise AtomBeeError('must have source')
        payload['title'] = title
        payload['desc'] = desc
        payload['desc_format_id'] = 0
        payload['copyright'] = 2
        payload['videos'] = [{'filename': middle.key.replace('.mp4', ''),
                              'title': self.file.URI,
                              'desc': ''}]
        payload['no_reprint'] = 1
        payload['tid'] = 157
        payload['cover'] = ''
        payload['tag'] = '美妆'
        payload['dynamic'] = ''
        payload['subtitle'] = {'open': 0, 'lan': ''}

        return payload

    def add(self, middle)->int:
        '''
        :return: aid

        :param :
        '''
        csrf = self.bee.cookies['bili_jct']
        print(f'csrf: {csrf}')
        endpoint = self.config.endpoints['add'] + f'?csrf={csrf}'
        payload = self.buildPayload(middle)
        # debug
        print(f'payload : {payload}')
        # TODO fix this
        # print(f'preAdd success: {self.preAdd()}')
        try:
            resp = requests.post(endpoint, json=payload,
                                 cookies=self.bee.cookies)
            if 'data' in resp.text:
                aid = json.loads(resp.text)['data']['aid']
                return int(aid)
        except Exception:
            return 0
