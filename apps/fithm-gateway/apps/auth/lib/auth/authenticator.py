from .base import AuthBase


class Authenticator(AuthBase):
    '''Authenticator'''

    def __init__(self):
        AuthBase.__init__(self)
