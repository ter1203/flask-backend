from flask import current_app, g


class TradeView:

    def __init__(self):
        pass


    def get_trades(self) -> list:
        '''Get all trades'''

        return f'all_trades'


    def create_trade(self, body: dict) -> dict:
        '''Create a new trade'''

        return body


    def get_trade(self, id: int) -> dict:
        '''Get a trade details'''

        return f'trade_{id}'


    def update_trade(self, id: int, body: dict) -> dict:
        '''Update a trade'''

        return f'update trade_{id}'


    def delete_trade(self, id: int):
        '''Delete a trade'''

        return f'delete trade_{id}'


    def get_instructions(self, body: dict) -> list:
        '''Get instructions'''

        return 'get_instructions'


    def get_portfolios(self, id: int) -> list:
        '''Get portfolios for the trade'''

        return f'portfolios for trade_{id}'


    def get_positions(self, id: int) -> list:
        '''Get positions for the trade'''

        return f'positions for trade_{id}'


    def update_positions(self, id: int, body: dict) -> dict:
        '''Update positions for the trade'''

        return f'update_positions for trade_{id}'


    def get_prices(self, id: int) -> list:
        '''Get prices for the trade'''

        return f'prices for trade_{id}'


    def update_prices(self, id: int, body: dict) -> dict:
        '''Update prices for the trade'''

        return f'update prices for trade_{id}'


    def get_requests(self, id: int) -> list:
        '''Get all requests for the trade'''

        return f'requests for trade_{id}'
