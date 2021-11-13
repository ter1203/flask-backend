from flask_restx import reqparse
from flask import Request


class AccountParser:
    '''Account endpoints arguments parser'''

    def __init__(self):
        self.create = None
        self.list = None
        self.update = None


    def parse_create(self, req: Request) -> dict:
        if not self.create:
            self.create = reqparse.RequestParser()
            self.create.add_argument('broker_name', required=True, type=str, location='json')
            self.create.add_argument('account_number', required=True, type=str, location='json')
            self.create.add_argument('portfolio_id', type=str, location='json')

        return self.create.parse_args(req)
