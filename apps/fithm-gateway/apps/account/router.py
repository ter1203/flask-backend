from flask_restx import Namespace, Resource

account = Namespace('account', path='/accounts')


@account.route('/<user_id>')
class Accounts(Resource):
    
    @account.doc('get accounts')
    def get(self, user_id: str):
        '''List all accounts'''

        return f'Welcome {user_id}'