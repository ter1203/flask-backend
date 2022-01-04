from flask_restx import Namespace, Resource
from flask import request
from .view import AccountView

account = Namespace('account', path='/accounts')
view = AccountView()

@account.route('')
class Accounts(Resource):

    @account.doc('get accounts')
    def get(self):
        '''List all accounts'''

        return view.get_accounts()


    @account.doc('create account')
    def post(self):
        '''Create an account for a user'''

        return view.create_account(request.json)


@account.route('/<int:account_id>')
class Account(Resource):

    @account.doc('get account info')
    def get(self, account_id: str):

        return view.get_account(account_id)


    @account.doc('update account info')
    def put(self, account_id: str):

        return view.update_account(account_id, request.json)


    @account.doc('delete account')
    def delete(self, account_id: str):

        return view.delete_account(account_id)
