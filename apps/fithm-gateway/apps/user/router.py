from flask_restx import Namespace, Resource
from flask import request
from .lib.parser import AuthParser
from .lib.validator import AuthValidator
from .view import UserView
from libs.depends.entry import container


user = Namespace('user', path='/auth')
view = UserView()

@user.route('/')
class Users(Resource):

    @user.doc('user healthy')
    def get(self):
        '''List all users'''

        return f'Welcome user'


@user.route('/signup')
class Signup(Resource):
    '''Sign up'''

    @user.doc('sign-up new user')
    def post(self):

        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_signup(request)

        validator: AuthValidator = container.get(AuthValidator)
        validator.validate_signup(param)

        return param
        # return view.signup(param)
