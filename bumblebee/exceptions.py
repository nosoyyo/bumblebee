class BumbleBeeError(Exception):

    errmsgs = {
        101: '_GET: resp not ok.',
        102: '_GET: cannot decode JSON.',
        103: '_POST: resp not ok.',
        104: '_POST: cannot decode JSON.'
    }

    def __init__(self, err_code=None):
        if not err_code:
            print('no err_code')
        else:
            msg = self.errmsgs[err_code]
            print(f'Error: {msg}')


class BumbleBeeAnswerError(BumbleBeeError):
    errmsgs = {
        201: 'Answer.__init__: must contain "answer_id" or "doc"',
        202: 'Answer.aloha: this id is not in MongoDB',
    }
