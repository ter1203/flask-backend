from flask_restx import reqparse
from flask import Request


class ModelParser():

    def __init__(self):
        self.get = None
        self.create = None
        self.update_pos = None


    def parse_get_list(self, req: Request) -> dict:
        if not self.get:
            self.get = reqparse.RequestParser()
            self.get.add_argument('public', type=bool, location='args')

        return self.get.parse_args(req)


    def parse_create(self, req: Request) -> dict:
        if not self.create:
            self.create = reqparse.RequestParser()
            self.create.add_argument('name', type=str, location='json')
            self.create.add_argument('keywords', type=str, location='json')
            self.create.add_argument('public', type=str, location='json')

        return self.create.parse_args(req)


    def parse_update_positions(self, req: Request) -> dict:
        if not self.update_pos:
            self.update_pos = reqparse.RequestParser()
            self.update_pos.add_argument('positions', type=list, location='json')

        return self.update_pos.parse_args(req)
