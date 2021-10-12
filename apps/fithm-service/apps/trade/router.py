from flask_restx import Namespace, Resource

trade = Namespace('trade', path='/trades')


@trade.route('/')
class Trades(Resource):

    @trade.doc('trade healthy')
    def get(self):
        '''List all trades'''

        return f'Welcome trade'
