from flask_restx import Namespace, Resource
from flask import request
from .lib.parser import AuthParser
from .lib.validator import AuthValidator
from .view import AuthView
from libs.depends.entry import container
from libs.middleware.auth import login_required


auth = Namespace('auth', path='/auth')
view = AuthView()


@auth.route('/signup')
class Signup(Resource):
    '''User signup'''

    @auth.doc('sign-up new user')
    def post(self):

        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_signup(request)

        validator: AuthValidator = container.get(AuthValidator)
        validator.validate_signup(param)

        return view.signup(param)


@auth.route('/signin')
class Signin(Resource):
    '''Sign in'''

    def post(self):
        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_signin(request)

        validator: AuthValidator = container.get(AuthValidator)
        validator.validate_signin(param)

        return view.signin(param['email'], param['password'])


@auth.route('/signout')
class Signout(Resource):
    '''Sign out'''

    @login_required()
    def post(self):
        
        return view.signout()


@auth.route('/confirm-email')
class ConfirmEmail(Resource):
    '''Confirm mail'''

    def post(self):

        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_email_confirm(request)

        return view.confirm(param['confirm_token'])


@auth.route('/send-confirm')
class SendConfirm(Resource):
    '''Send confirmation email'''

    @login_required()
    def get(self):

        return view.send_confirm()


@auth.route('/forgot-password')
class ForgotPassword(Resource):
    '''Send reset password link'''

    def post(self):
        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_forgot_password(request)

        return view.forgot_password(param['email'])


@auth.route('/reset-password')
class ResetPassword(Resource):

    def post(self):
        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_reset_password(request)

        return view.reset_password(param['reset_token'], param['password'])


@auth.route('/refresh')
class RefreshToken(Resource):

    def get(self):
        parser: AuthParser = container.get(AuthParser)
        param = parser.parse_refresh(request)

        return view.refresh(param['token'])
