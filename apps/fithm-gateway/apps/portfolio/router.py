from flask_restx import Namespace, Resource
from flask import request
from libs.helper.forward import forward_request
from libs.middleware.auth import login_required, active_required
from libs.depends.entry import container
from .lib.parser import PortfolioParser

portfolio = Namespace('portfolio', path='/portfolios', decorators=[active_required(), login_required()])

@portfolio.route('')
class PortfolioList(Resource):

    @portfolio.doc('get all portfolios')
    def get(self):
        '''List all portfolios'''

        return forward_request()


    @portfolio.doc('create a portfolio')
    def post(self):
        
        parser: PortfolioParser = container.get(PortfolioParser)
        body = parser.parse_create(request)

        return forward_request(body=body)


@portfolio.route('/<int:port_id>')
class Portfolio(Resource):

    @portfolio.doc('get a portfolio')
    def get(self, port_id: int):

        return forward_request()


    @portfolio.doc('update a portfolio')
    def put(self, port_id: int):

        parser: PortfolioParser = container.get(PortfolioParser)
        body = parser.parse_create(request)

        return forward_request(body=body)


    @portfolio.doc('delete a portfolio')
    def delete(self, port_id: int):

        return forward_request()


@portfolio.route('/<int:port_id>/accounts')
class PortfolioAccounts(Resource):

    @portfolio.doc('update the portfolio accounts')
    def put(self, port_id: int):

        parser: PortfolioParser = container.get(PortfolioParser)
        body = parser.parse_update_account(request)

        return forward_request(body=body)


@portfolio.route('/<int:port_id>/model')
class PortfolioModel(Resource):

    @portfolio.doc('update the portfolio model')
    def put(self, port_id: int):

        parser: PortfolioParser = container.get(PortfolioParser)
        body = parser.parse_update_model(request)

        return forward_request(body=body)
