from flask_restx import reqparse
from flask import Request

class AuthParser:
    
    def __init__(self) -> None:
        self.signup = None
        self.update = None
        self.signin = None
        self.email_confirm = None
        self.forgot_pass = None
        self.reset_pass = None


    def parse_signup(self, req: Request) -> dict:
        if not self.signup:
            self.signup = reqparse.RequestParser()
            self.signup.add_argument('email', required=True, type=str, location='json')
            self.signup.add_argument('username', required=True, type=str, location='json')
            self.signup.add_argument('password', required=True, type=str, location='json')

        return self.signup.parse_args(req)


    def parse_update(self, req: Request) -> dict:
        if not self.update:
            self.update = reqparse.RequestParser()
            self.update.add_argument('first_name', type=str, location='json')
            self.update.add_argument('last_name', type=str, location='json')
            self.update.add_argument('company', type=str, location='json')
            self.update.add_argument('phone_number', type=str, location='json')

        return self.update.parse_args(req)


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


    def parse_forgot_password(self, req: Request) -> dict:
        if not self.forgot_pass:
            self.forgot_pass = reqparse.RequestParser()
            self.forgot_pass.add_argument('email', required=True, type=str, location='json')

        return self.forgot_pass.parse_args(req)


    def parse_reset_password(self, req: Request) -> dict:
        if not self.reset_pass:
            self.reset_pass = reqparse.RequestParser()
            self.reset_pass.add_argument('reset_token', required=True, type=str, location='json')
            self.reset_pass.add_argument('password', required=True, type=str, location='json')

        return self.reset_pass.parse_args(req)
