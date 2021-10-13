from flask import abort
from libs.validators import email_is_valid, password_is_valid

class AuthValidator:

    def validate_signup(self, param: dict) -> dict:

        self.__validate_email(param)
        self.__validate_password(param)

        if not param['username']:
            abort(400, 'Invalid username')


    def validate_signin(self, param: dict) -> dict:
        
        self.__validate_email(param)
        self.__validate_password(param)


    def __validate_email(self, param: dict):
         if not email_is_valid(param['email']):
            abort(400, 'Invalid email address')


    def __validate_password(self, param: dict):
        if not password_is_valid(param['password']):
            abort(400, 'Invalid password')