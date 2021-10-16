from flask_restx import Namespace, Resource
from flask import request
from .view import PortfolioView

portfolio = Namespace('portfolio', path='/portfolios')
view = PortfolioView()

@portfolio.route('')
class PortfolioList(Resource):

    @portfolio.doc('get all portfolios')
    def get(self):
        '''List all portfolios'''

        return view.get_portfolios()


    @portfolio.doc('create a portfolio')
    def post(self):
        
        return view.create_portfolio(request.json)


@portfolio.route('/<int:port_id>')
class Portfolio(Resource):

    @portfolio.doc('get a portfolio')
    def get(self, port_id: int):

        return view.get_portfolio(port_id)


    @portfolio.doc('update a portfolio')
    def put(self, port_id: int):

        return view.update_portfolio(port_id, request.json)


    @portfolio.doc('delete a portfolio')
    def delete(self, port_id: int):

        return view.delete_portfolio(port_id)


@portfolio.route('/<int:port_id>/accounts')
class PortfolioAccounts(Resource):

    @portfolio.doc('update the portfolio accounts')
    def put(self, port_id: int):

        return view.update_accounts(port_id, request.json)


@portfolio.route('/<int:port_id>/model')
class PortfolioModel(Resource):

    @portfolio.doc('update the portfolio model')
    def put(self, port_id: int):

        return view.update_model(port_id, request.json)
