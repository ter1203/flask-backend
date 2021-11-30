from flask import current_app
import requests as req
from typing import Optional


QUOVO_BASE = 'https://api.quovo.com/v3'

class QuovoRequest:

    def __init__(self):
        self.headers = None


    def get(self, path: str, params: Optional[dict] = None):
        '''Get request to quovo'''

        headers = self.__get_default_headers()
        return req.get(QUOVO_BASE + path, headers=headers, params=params)


    def post(self, path: str, body: dict, params: Optional[dict] = None):
        '''Post request to quovo'''

        headers = self.__get_default_headers()
        headers = {**headers, 'Content-Type': 'application/json'}

        return req.post(QUOVO_BASE + path, headers=headers, params=params, data=body)


    def put(self, path: str, body: dict, params: Optional[dict] = None):
        '''Put request to quovo'''

        headers = self.__get_default_headers()
        headers = {**headers, 'Content-Type': 'application/json'}

        return req.post(QUOVO_BASE + path, headers=headers, params=params, data=body)


    def delete(self, path: str, params: Optional[dict] = None):
        '''Delete request to quovo'''

        headers = self.__get_default_headers()
        return req.post(QUOVO_BASE + path, headers=headers, params=params)


    def __get_default_headers(self):
        '''Get default header including authorization'''

        if not self.headers:
            self.headers = {
                'Authorization': f'Bearer {current_app.config["FITHM_QUOVO_KEY"]}'
            }

        return self.headers
