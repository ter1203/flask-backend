from flask import abort
from libs.validators import email_is_valid, password_is_valid

class AuthValidator:

    def validate_signup(self, param: dict) -> dict:

        if not email_is_valid(param['email']):
            abort(400, 'Invalid email address')

        if not password_is_valid(param['password']):
            abort(400, 'Invalid password')
