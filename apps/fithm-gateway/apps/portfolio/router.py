from flask_restx import Namespace, Resource

portfolio = Namespace('portfolio', path='/portfolios')

@portfolio.route('/')
class Portfolios(Resource):

    @portfolio.doc('portfolio healthy')
    def get(self):
        '''List all portfolios'''

        return f'Welcome portfolio'