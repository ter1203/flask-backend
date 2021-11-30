from flask import current_app
import requests as req
from apps.models import User
from libs.depends.entry import container
from .base import QuovoRequest


def new_positions_with_account(positions: list, broker: str, account_number: str) -> list:
    '''Set account info(broker name and account number) to positions'''

    return [{
        'symbol': pos['symbol'] if pos['symbol'] != 'CUR:USD' else 'account_cash',
        'broker_name': broker,
        'shares': pos['quantity'],
        'account_number': account_number
    } for pos in positions]


def delete_quovo_user(quovo_user_id: str):

    request: QuovoRequest = container.get(QuovoRequest)
    return request.delete(f'/users/{quovo_user_id}')


def get_quovo_holdings(accounts: list):
    '''Get account holdings'''

    updated_positions = []
    request: QuovoRequest = container.get(QuovoRequest)
    for account in accounts:
        number: str = account['account_number']
        if not number.startswith('quovo_'):
            continue

        result = request.get(f'/accounts/{account["account_number"][6:]}/holdings')
        positions = new_positions_with_account(
            result['holdings'],
            account['broker_name'],
            account['account_number']
        )

        updated_positions.extend(positions)

    return updated_positions



def set_quovo_account_list(user: User, quovo_response, manual=None):
    new_list = [{'broker_name': r['institution_name'],
                 'account_number': 'quovo_' + str(r['id'])} for r in quovo_response]
    if manual:
        new_list.extend(manual)
    return req.post(
        current_app.config['API_BASE_URL'] + '/account/user_accounts/' + user.tradeshop_id,
        json={'account_list': new_list}).json()
