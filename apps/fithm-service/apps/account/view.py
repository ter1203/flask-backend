from typing import List
from flask import current_app, g, abort
from libs.database import db_session
from .models import Account
from apps.models import Business

class AccountView:

    def __init__(self):
        pass


    def get_accounts(self):
        '''Get all accounts owned by user'''

        business: Business = g.business
        accounts: List[Account] = business.accounts
        return {
            'accounts': [account.as_dict() for account in accounts]
        }


    def create_account(self, body: dict) -> dict:
        '''Create a new account for the user'''

        # check existence
        accounts = db_session.query(Account).filter(
            Account.broker_name == body['broker_name'],
            Account.account_number == body['account_number']
        ).all()
        if len(accounts):
            abort(403, 'Account already exists')

        # create an account
        account = Account(
            business_id=g.business.id,
            broker_name=body['broker_name'],
            account_number=body['account_number']
        )
        if 'portfolio_id' in body and body['portfolio_id']:
            account.portfolio_id = body['portfolio_id']

        db_session.add(account)
        db_session.commit()

        return account.as_dict()


    def get_account(self, id: int):
        '''Get account detail'''

        account = self.__get_account(id)
        return account.as_dict()


    def delete_account(self, id: int):
        '''Delete an account'''

        account = self.__get_account(id)
        db_session.delete(account)
        db_session.commit()

        return {
            'result': 'success'
        }


    def __get_account(id: int) -> Account:

        account = db_session.query(Account).get(id)
        if not account:
            abort(404, 'Account not found')
        if account.business_id != g.business.id:
            abort(403, "You don't have permission to this account.")

        return account
