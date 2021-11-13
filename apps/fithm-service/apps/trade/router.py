from flask_restx import Namespace, Resource
from flask import request
from .view import TradeView

trade = Namespace('trade', path='/trades')
view = TradeView()

@trade.route('')
class TradeList(Resource):

    @trade.doc('get trade list')
    def get(self):
        '''List all trades'''

        return view.get_trades()


    @trade.doc('create a trade')
    def post(self):

        return view.create_trade(request.json)


@trade.route('/instructions')
class TradeInstructions(Resource):

    @trade.doc('get instructions')
    def post(self):

        return view.get_instructions(request.json)


@trade.route('/<int:trade_id>')
class Trade(Resource):

    @trade.doc('get trade')
    def get(self, trade_id: int):

        return view.get_trade(trade_id)


    @trade.doc('delete a trade')
    def delete(self, trade_id: int):

        return view.delete_trade(trade_id)


    @trade.doc('update a trade')
    def put(self, trade_id: int):

        return view.update_trade(trade_id, request.json)


@trade.route('/<int:trade_id>/portfolios')
class TradePortfolios(Resource):

    @trade.doc('add portfolios')
    def post(self, trade_id: int):

        return view.update_portfolios(trade_id, request.json)


@trade.route('/<int:trade_id>/positions')
class TradePositions(Resource):

    @trade.doc('get positions')
    def get(self, trade_id: int):

        args = request.args
        return view.get_positions(trade_id, args)


    @trade.doc('update positions')
    def put(self, trade_id: int):

        return view.update_positions(trade_id, request.json)


@trade.route('/<int:trade_id>/prices')
class TradePrices(Resource):

    @trade.doc('get prices')
    def get(self, trade_id: int):

        return view.get_prices(trade_id)


    @trade.doc('update iex prices')
    def post(self, trade_id: int):

        return view.update_prices(trade_id, request.json)


@trade.route('/<int:trade_id>/requests')
class TradeRequests(Resource):

    @trade.doc('get requests')
    def get(self, trade_id: int):

        return view.get_requests(trade_id)
