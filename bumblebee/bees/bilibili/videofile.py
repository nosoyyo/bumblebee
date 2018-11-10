__doc__ = 'baidubce 2to3 by nosoyyo'
__version__ = 'baidubce for py3 ver 2c374'
import os

from config import Bilibili

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


class VideoFile():
    '''
    For upload & add single file upon bilibili.com
    '''

    config = Bilibili()
    cu = os.getlogin()
    full_path = f'/Users/{cu}/{config.default_dir}'
    preupload_params = config.preupload_params

    def __init__(self, file_name):
        '''
        : param file_name: looks like 'a42b4aa9aa1a47ad8bb2c02a57b60482.mp4'
        '''
        if '.mp4' in file_name:
            self.URI = file_name.replace('.mp4', '')
            self.file_name = file_name
        else:
            self.URI = file_name
            self.file_name = f'{file_name}.mp4'
        self.full_name = f'{self.config.full_path}/{file_name}'
