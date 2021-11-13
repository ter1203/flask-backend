from flask_restx import reqparse
from flask import Request

class UserParser:
    
    def __init__(self) -> None:
        self.update = None


    def parse_update(self, req: Request) -> dict:
        if not self.update:
            self.update = reqparse.RequestParser()
            self.update.add_argument('email', type=str, location='json')
            self.update.add_argument('first_name', type=str, location='json')
            self.update.add_argument('last_name', type=str, location='json')
            self.update.add_argument('company', type=str, location='json')
            self.update.add_argument('phone_number', type=str, location='json')
            self.update.add_argument('old_password', type=str, location='json')
            self.update.add_argument('new_password', type=str, location='json')

        return self.update.parse_args(req)
