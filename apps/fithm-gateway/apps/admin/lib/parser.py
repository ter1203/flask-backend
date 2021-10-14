from flask_restx import reqparse
from flask import Request


class AdminParser:
    '''Admin endpoints arguments parser'''

    def __init__(self):
        self.get_users = None


    def parse_get_users(self, req: Request) -> dict:
        if not self.get_users:
            self.get_users = reqparse.RequestParser()
            self.get_users.add_argument(
                'page', default=1, type=int, location='args')
            self.get_users.add_argument(
                'page_size', default=10, type=int, location='args')

        return self.get_users.parse_args(req)
