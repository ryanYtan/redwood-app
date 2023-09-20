import enum

class ResponseCode(str, enum.Enum):
    SUCCESS = 'SUCCESS'
    ERR_BAD_REQUEST = 'ERR_BAD_REQUEST'
    ERR_USER_ALREADY_EXISTS = 'ERR_USER_ALREADY_EXISTS'
    ERR_FAILED_LOGIN = 'ERR_FAILED_LOGIN'
    ERR_NOT_FOUND = 'ERR_NOT_FOUND'
    ERR_USER_UNLOGGED = 'ERR_USER_UNLOGGED'


class Response:
    def __init__(self, code, message = '', data = None):
        self.code = code
        self.message = message
        self.data = data

    def dict(self):
        return { 'code': self.code, 'message': self.message, 'data': self.data }
