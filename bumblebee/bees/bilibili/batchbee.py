class BiliBatchBee():

    def __init__(self):
        pass

    def checkVideos(self, path: str = None) -> list:
        '''
        NOT FOR THIS CLASS
        SHOULD BE MOVED TO BATCH CLASS
        check the default path, collect videos for uploading.

        : return: a `list` of video file path(s)
        '''
        _dir = path or self.config.full_path
        return [f for f in os.listdir(_dir) if f.endswith('.mp4')]
