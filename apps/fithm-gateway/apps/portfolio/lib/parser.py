from flask_restx import reqparse
from flask import Request

class PortfolioParser():

    def __init__(self):
        self.create = None
        self.update_account = None
        self.update_model = None


    def parse_create(self, req: Request) -> dict:
        if not self.create:
            self.create = reqparse.RequestParser()
            self.create.add_argument('name', type=str, required=True, location='json')
            # self.create.add_argument('model_id', type=int, location='json')

        return self.create.parse_args(req)


    def parse_update_account(self, req: Request) -> dict:
        if not self.update_account:
            self.update_account = reqparse.RequestParser()
            self.update_account.add_argument('accounts', type=list, required=True, location='json')

        return self.update_account.parse_args(req)


    def parse_update_model(self, req: Request) -> dict:
        if not self.update_model:
            self.update_model = reqparse.RequestParser()
            self.update_model.add_argument('model_id', type=int, required=True, location='json')

        return self.update_model.parse_args(req)
