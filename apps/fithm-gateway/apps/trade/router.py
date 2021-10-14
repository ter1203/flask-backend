from flask_restx import Namespace, Resource
from flask import request
from libs.helper.forward import forward_request
from libs.middleware.auth import login_required, active_required
from libs.depends.entry import container
from .lib.parser import TradeParser

trade = Namespace('trade', path='/trades', decorators=[active_required(), login_required()])


@trade.route('')
class TradeList(Resource):

    @trade.doc('get trade list')
    def get(self):
        '''List all trades'''

        return forward_request()


    @trade.doc('create a trade')
    def post(self):

        return forward_request()


@trade.route('/instructions')
class TradeInstructions(Resource):

    @trade.doc('get trades')
    def post(self):

        parser: TradeParser = container.get(TradeParser)
        body = parser.parse_instructions(request)

        return forward_request(body=body)


@trade.route('/<int:trade_id>')
class Trade(Resource):

    @trade.doc('get trade')
    def get(self, trade_id: int):

        return forward_request()


    @trade.doc('delete a trade')
    def delete(self, trade_id: int):

        return forward_request()


    @trade.doc('update a trade')
    def put(self, trade_id: int):

        parser: TradeParser = container.get(TradeParser)
        body = parser.parse_update()

        return forward_request(body=body)


@trade.route('/<int:trade_id>/portfolios')
class TradePortfolios(Resource):

    @trade.doc('add portfolios')
    def post(self, trade_id: int):

        parser: TradeParser = container.get(TradeParser)
        body = parser.parse_update_portfolios(request)

        return forward_request(body=body)


@trade.route('/<int:trade_id>/positions')
class TradePositions(Resource):

    @trade.doc('get positions')
    def get(self, trade_id: int):

        return forward_request()


    @trade.doc('update positions')
    def put(self, trade_id: int):

        parser: TradeParser = container.get(TradeParser)
        body = parser.parse_update_positions(request)

        return forward_request(body=body)


@trade.route('/<int:trade_id>/prices')
class TradePrices(Resource):

    @trade.doc('get prices')
    def get(self, trade_id: int):

        return forward_request()


    @trade.doc('update iex prices')
    def post(self, trade_id: int):

        parser: TradeParser = container.get(TradeParser)
        body = parser.parse_update_positions(request)

        return forward_request(body=body)


@trade.route('/<int:trade_id>/requests')
class TradeRequests(Resource):

    @trade.doc('get requests')
    def get(self):

        return forward_request()
