from datetime import datetime
from flask import current_app, g
from libs.database import db_session, helpers
from libs.database.portfolios import get_portfolios
from libs.database.trade import (
    update_account_positions, get_trade_prices,
    update_trade_prices, get_requests
)
from libs.database.accounts import get_account_positions
from apps.models import Trade, Business, Portfolio, Pending, AccountPosition


class TradeView:

    def __init__(self):
        pass


    def get_trades(self) -> list:
        '''Get all trades'''

        business: Business = g.business
        return {
            'trades': [trade.as_dict() for trade in business.trades]
        }


    def create_trade(self, param: dict) -> dict:
        '''Create a new trade'''

        name = param['name']
        trade = Trade(
            business_id=g.business.id,
            name=name,
            status=False,
            created=datetime.utcnow()
        )
        db_session.add(trade)
        db_session.commit()

        return trade.as_dict()


    def get_trade(self, id: int) -> dict:
        '''Get a trade details'''

        trade = self.__get_trade(id)
        return trade.as_dict()


    def update_trade(self, id: int, body: dict) -> dict:
        '''Update a trade'''

        status = body['status']
        name = body['name']
        trade = self.__get_trade(id)
        trade.name = name
        trade.status = status
        db_session.commit()

        return trade.as_dict()


    def delete_trade(self, id: int):
        '''Delete a trade'''

        pendings = db_session.query(Pending).filter(Pending.trade_id == id)

        trade = self.__get_trade(id)
        db_session.delete(trade)
        db_session.commit()

        helpers.update_trades_for_pendings(pendings)
        return { 'result': 'success' }


    def get_instructions(self, body: dict) -> list:
        '''Get instructions'''

        return 'Not implemented yet'


    def update_portfolios(self, id: int, body: dict) -> list:
        '''Get portfolios for the trade'''

        trade = self.__get_trade(id)
        port_ids = body['portfolios']

        helpers.trade_update_portfolios(trade, get_portfolios(port_ids))
        return trade.as_dict()


    def get_positions(self, id: int, args: dict) -> list:
        '''Get positions for the trade'''

        trade = self.__get_trade(id)
        if 'portfolio_id' in args and args['portfolio_id']:
            portfolio = db_session.query(Portfolio).get(args['portfolio_id'])
            positions = portfolio.account_positions
        else:
            pendings: list[Pending] = trade.pendings
            ids = [pending.id for pending in pendings]
            positions = db_session.query(AccountPosition).filter(
                AccountPosition.pending_id.in_(ids)
            ).all()

        return [position.as_dict() for position in positions]


    def update_positions(self, id: int, body: dict) -> dict:
        '''Update positions for the trade'''

        positions = body['positions']
        trade = self.__get_trade(id)
        positions: list[AccountPosition] = get_account_positions(positions)
        update_account_positions(trade, positions)

        return self.__get_trade(id).as_dict()


    def get_prices(self, id: int) -> list:
        '''Get prices for the trade'''

        trade = self.__get_trade(id)
        prices = get_trade_prices(trade)
        if prices is None:
            return []
        else:
            return [p.as_dict() for p in prices['price_object']]


    def update_prices(self, id: int, body: dict) -> dict:
        '''Update prices for the trade'''

        if 'iex' not in body or not body['iex']:
            prices = None
        else:
            prices = body['prices']
        
        trade = self.__get_trade(id)
        result = update_trade_prices(trade, prices)

        if isinstance(result, str):
            return {'error': result}, 400
        else:
            return self.__get_trade(id).as_dict()


    def get_requests(self, id: int) -> list:
        '''Get all requests for the trade'''

        trade = self.__get_trade(id)
        return {
            'requests': get_requests(trade)
        }


    def __get_trade(self, id: int) -> Trade:

        return db_session.query(Trade).get(id)
