from flask_restx import Namespace, Resource
import requests
from libs.middleware.auth import login_required, active_required

account = Namespace('account', path='/accounts', decorators=[active_required(), login_required()])


@account.route('/')
class Accounts(Resource):

    @account.doc('get accounts')
    def get(self):
        '''List all accounts'''

        return f'Welcome list'


    @account.doc('create account')
    def post(self):
        '''Create an account for a user'''

        return 'Create an account'