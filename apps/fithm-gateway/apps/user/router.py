from flask_restx import Namespace, Resource
from flask import request, g
from .lib.parser import AuthParser
from .lib.validator import AuthValidator
from .view import UserView
from libs.depends.entry import container
from libs.middleware.auth import login_required


user = Namespace('user', path='/auth')
view = UserView()


@user.route('/signup')
class Signup(Resource):
    '''Sign up'''

    @user.doc('sign-up new user')
    def post(self):

        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_signup(request)

        validator: AuthValidator = container.get(AuthValidator)
        validator.validate_signup(param)

        return view.signup(param)


@user.route('/signin')
class Signin(Resource):
    '''Sign in'''

    def post(self):
        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_signin(request)

        validator: AuthValidator = container.get(AuthValidator)
        validator.validate_signin(param)

        return view.signin(param['email'], param['password'])


@user.route('/signout')
class Signout(Resource):
    '''Sign out'''

    @login_required()
    def post(self):
        
        return view.signout()


@user.route('/confirm-email')
class ConfirmEmail(Resource):
    '''Confirm mail'''

    def post(self):

        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_email_confirm(request)

        return view.confirm(param['confirm_token'])


@user.route('/send-confirm')
class SendConfirm(Resource):
    '''Send confirmation email'''

    @login_required()
    def get(self):

        return view.send_confirm()
