from flask_restx import Namespace, Resource
from flask import request, current_app
from .lib.parser import AccountParser
from libs.depends.entry import container
from libs.helper.forward import forward_request

from libs.middleware.auth import login_required, active_required

account = Namespace('account', path='/accounts', decorators=[active_required(), login_required()])

@account.route('/')
class Accounts(Resource):

    @account.doc('get accounts')
    def get(self):
        '''List all accounts'''

        result = forward_request()
        return f'Welcome {result}'


    @account.doc('create account')
    def post(self):
        '''Create an account for a user'''

        parser: AccountParser = container.get(AccountParser)
        param = parser.parse_create(request)

        return f'Create an account: {param}'


@account.route('/<account_id>')
class Account(Resource):

    @account.doc('get account info')
    def get(self, account_id: str):

        return f'Welcome {account_id}'


    @account.doc('delete account')
    def delete(self, account_id: str):

        return f'Delete {account_id}'
    