from flask import current_app, g


class AccountView:

    def __init__(self):
        pass


    def get_accounts(self):
        '''Get all accounts owned by user'''

        return f'get_accounts: {g.user}'


    def create_account(self, body: dict) -> dict:
        '''Create a new account for the user'''

        return f'create_account'


    def get_account(self, id: int):
        '''Get account detail'''

        return f'account_{id}'


    def delete_account(self, id: int):
        '''Delete an account'''

        return f'delect account_{id}'
