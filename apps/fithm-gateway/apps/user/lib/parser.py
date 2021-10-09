from flask_restx import reqparse
from flask import Request

class AuthParser:
    
    def __init__(self) -> None:
        self.signup = None
        self.signin = None
        self.email_confirm = None


    def parse_signup(self, req: Request) -> dict:
        if not self.signup:
            self.signup = reqparse.RequestParser()
            self.signup.add_argument('email', required=True, type=str, location='json')
            self.signup.add_argument('username', type=str, location='json')
            self.signup.add_argument('password', required=True, type=str, location='json')

        return self.signup.parse_args(req)


    def parse_signin(self, req: Request) -> dict:
        if not self.signin:
            self.signin = reqparse.RequestParser()
            self.signin.add_argument('email', required=True, type=str, location='json')
            self.signin.add_argument('password', required=True, type=str, location='json')

        return self.signin.parse_args(req)


    def parse_email_confirm(self, req: Request) -> dict:
        if not self.email_confirm:
            self.email_confirm = reqparse.RequestParser()
            self.email_confirm.add_argument('confirm_token', required=True, type=str, location='json')

        return self.email_confirm.parse_args(req)
