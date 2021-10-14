from flask import current_app, g


class PortfolioView:

    def __init__(self):
        pass


    def get_portfolios(self):
        '''Get all portfolios'''

        return f'get_portfolios'


    def create_portfolio(self, body: dict) -> dict:
        '''Create a new portfolio'''

        return body


    def get_portfolio(self, id: int) -> dict:
        '''Get portfolio details'''

        return f'portfolio_{id}'


    def update_portfolio(self, id: int, body: dict) -> dict:
        '''Update a portfolio'''

        return f'update portfolio_{id}'


    def delete_portfolio(self, id: int):
        '''Delete a portfolio'''

        return f'delete portfolio_{id}'


    def get_accounts(self, id: int):
        '''Get accounts connected to the porfolio'''

        return f'accounts for portfolio_{id}'


    def get_models(self, id: int):
        '''Get models connected to the portfolio'''

        return f'models for portfolio_{id}'
