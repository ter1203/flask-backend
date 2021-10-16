from flask import current_app, g
from apps.models import Portfolio, Business, Model
from libs.database import db_session, helpers
from libs.database.accounts import get_accounts

class PortfolioView:

    def __init__(self):
        pass


    def get_portfolios(self):
        '''Get all portfolios'''

        business: Business = g.business
        return {
            'portfolios': business.portfolios
        }


    def create_portfolio(self, body: dict) -> dict:
        '''Create a new portfolio'''

        portfolio = Portfolio(
            name=body['name'],
            business_id=g.business.id
        )

        db_session.add(portfolio)
        db_session.commit()

        return portfolio.as_dict()


    def get_portfolio(self, id: int) -> dict:
        '''Get portfolio details'''

        return self.__get_portfolio(id)


    def update_portfolio(self, id: int, body: dict) -> dict:
        '''Update a portfolio'''

        portfolio = self.__get_portfolio(id)
        portfolio.name = body['name']
        db_session.commit()

        return portfolio.as_dict()


    def delete_portfolio(self, id: int):
        '''Delete a portfolio'''

        portfolio = self.__get_portfolio(id)
        pendings = portfolio.pendings
        
        db_session.delete(portfolio)
        helpers.update_trade_for_portfolio_model(pendings, False)

        return {'result': 'success'}


    def update_accounts(self, id: int, body: dict):
        '''Get accounts connected to the porfolio'''

        portfolio = self.__get_portfolio(id)
        pendings = portfolio.pendings
        if len(pendings) > 0:
            helpers.update_trade_for_portfolio_account(portfolio, pendings)

        account_ids = body['accounts']
        accounts = get_accounts(account_ids)
        portfolio.accounts = accounts
        db_session.commit()

        return portfolio.as_dict()


    def update_model(self, id: int, body: dict):
        '''Get models connected to the portfolio'''

        model_id = body['model_id']
        model = db_session.query(Model).get(model_id)
        portfolio = self.__get_portfolio(id)

        portfolio.model = model
        db_session.commit()

        pendings = portfolio.pendings
        if len(pendings) > 0:
            helpers.update_trade_for_portfolio_model(pendings)

        return portfolio.as_dict()


    def __get_portfolio(self, id: int):

        return db_session.query(Portfolio).get(id)
