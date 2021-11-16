from flask_restx import Namespace, Resource
from flask import request, current_app
from .lib.parser import AccountParser
from libs.depends.entry import container
from libs.helper.forward import forward_request
from libs.middleware.auth import login_required, active_required

account = Namespace('account', path='/accounts', decorators=[active_required(), login_required()])

@account.route('')
class Accounts(Resource):

    @account.doc('get accounts')
    def get(self):
        '''List all accounts'''

        return forward_request()


    @account.doc('create account')
    def post(self):
        '''Create an account for a user'''

        parser: AccountParser = container.get(AccountParser)
        param = parser.parse_create(request)

        return forward_request(body=param)


@account.route('/<int:account_id>')
class Account(Resource):

    @account.doc('get account info')
    def get(self, account_id: str):

        return forward_request()


    @account.doc('update account info')
    def put(self, account_id: str):
        '''Update an existing account'''

        parser: AccountParser = container.get(AccountParser)
        param = parser.parse_update(request)

        return forward_request(body=param)


    @account.doc('delete account')
    def delete(self, account_id: str):

        return forward_request()
    