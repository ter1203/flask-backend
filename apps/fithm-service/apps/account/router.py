from flask_restx import Namespace, Resource
from flask import request

account = Namespace('account', path='/accounts')


@account.route('/')
class Accounts(Resource):

    @account.doc('get accounts')
    def get(self):
        '''List all accounts'''

        return f'Welcome list'

    @account.doc('create account')
    def post(self):
        '''Create an account for a user'''

        param = request.json()
        return f'Create an account: {param}'


@account.route('/<account_id>')
class Account(Resource):

    @account.doc('get account info')
    def get(self, account_id: str):

        return f'Welcome {account_id}'

    @account.doc('delete account')
    def delete(self, account_id: str):

        return f'Delete {account_id}'
