from flask import current_app
from libs.database import db_session
from .portfolios import get_portfolios
from apps.models import (
    Trade, Business, Portfolio, Pending, 
    AccountPosition, Price, Account, Model,
    TradeRequest
)
import pandas as pd
from iexfinance.stocks import Stock
from datetime import datetime

def remove_all_pending_positions(trade: Trade):
    
    db_session.query(Price).filter(Price.trade_id == trade.id).delete(False)
    
    pending_ids = [p.id for p in trade.pendings]
    db_session.query(AccountPosition).filter(AccountPosition.pending_id.in_(pending_ids)).delete(False)
    db_session.commit()


def update_account_positions(trade: Trade, positions: list[AccountPosition]):

    if not len(positions):
        return remove_all_pending_positions(trade)

    new_positions, pending_positions = prepare_update(trade, positions)
    if new_positions != None:
        create_pending_account_positions(trade, new_positions, pending_positions)
        remove_pending_account_positions(new_positions, pending_positions)


def get_trade_prices(trade: Trade, use: str = 'read'):

    prices = trade.prices
    if len(prices) == 0:
        return None
    df_prices = pd.DataFrame(prices)
    df_prices.columns = ['price_object']
    df_price_details = pd.DataFrame([vars(p) for p in prices])
    if use == "read":
        obj_detail = pd.concat([df_prices, df_price_details], axis=1).drop_duplicates(
            subset=['symbol']
        )
    else:
        obj_detail = pd.concat([df_prices, df_price_details], axis=1)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(obj_detail)
    return obj_detail


def update_trade_prices(trade: Trade, prices = None):

    if prices is None:
        prices = get_iex(trade)
    price_unique = [dict(t) for t in {tuple(d.items()) for d in prices}]
    ext_symbols = list(set([a['symbol'] for a in prices]))
    if len(price_unique) != len(ext_symbols):
        return 'You have attempted to use different prices for the same security.'

    current_prices = get_trade_prices(trade, use="write")

    df_price_unique = pd.DataFrame(price_unique).set_index(['symbol'])
    current_prices = current_prices[
        current_prices['symbol'].isin([p['symbol'] for p in price_unique])
    ].drop('price', axis=1).set_index(['symbol'])
    current_prices['new_price'] = df_price_unique['price']

    def assign_it(row):
        row['price_object'].price = row['new_price']

    current_prices.apply(assign_it, axis=1)
    db_session.bulk_save_objects(current_prices['price_object'].tolist())
    db_session.commit()


def get_requests(trade: Trade, args: dict):

    # This request includes a bool to send the request to Trade Manager and save the trade request to the database.
    # body = request.get_json()

    # get all symbols from all models in trade
    pendings: list[Pending] = trade.pendings
    pending_ids = [p.id for p in pendings]
    positions = db_session.query(AccountPosition).filter(AccountPosition.pending_id.in_(pending_ids)).all()
    portfolio_ids = [p.portfolio_id for p in pendings]
    portfolio_objects = get_portfolios(portfolio_ids)

    if any([True if p.model_id is None else False for p in portfolio_objects]):
        return ValueError('One of your portfolios has not been assigned a model.')

    model_ids = [p.model_id for p in portfolio_objects]
    model_objects = db_session.query(Model).filter(Model.id.in_(model_ids)).all()
    # add portfolio_id to each model position
    for p in portfolio_objects:
        for m in model_objects:
            for a in m.allocation:
                if p.model_id == m.id:
                    a.portfolio_id = p.id
    model_allocations = [m.allocation for m in model_objects]
    all_model_symbols = []
    for allocation in model_allocations:
        model_symbols = [m for m in allocation]
        for m in model_symbols:
            all_model_symbols.append(m)

    df_model_positions = pd.DataFrame([vars(m) for m in all_model_symbols])
    df_model_positions.drop(['_sa_instance_state'], inplace=True, axis=1)
    df_model_positions.set_index(['portfolio_id'])

    df_account_positions = pd.DataFrame([vars(p) for p in positions])
    df_account_positions.drop(['_sa_instance_state'], inplace=True, axis=1)
    df_account_positions.set_index(['portfolio_id'])

    df_all_positions = pd.concat([df_model_positions, df_account_positions])
    df_all_positions.set_index(['symbol'], inplace=True)

    prices = trade.prices
    df_prices = pd.DataFrame([vars(p) for p in prices]).drop_duplicates(subset=['symbol'])
    df_prices.drop(['_sa_instance_state'], inplace=True, axis=1)
    df_prices.set_index(['symbol'], inplace=True)

    df_all_positions['price'] = df_prices['price']
    df_all_positions['restrictions'] = float('NaN')
    df_all_positions['trade_id'] = trade.id
    df_all_positions.rename(columns={'weight': 'model_weight'}, inplace=True)
    df_all_positions.reset_index(inplace=True)
    df_all_positions.account_number.fillna('model', inplace=True)

    all_requests = []
    for i, port in df_all_positions.groupby('portfolio_id'):
        trade_request_obj = {'portfolio_id': i}
        trade_request_obj['portfolio'] = df_all_positions.loc[:,
            ['account_number', 'symbol', 'shares', 'model_weight', 'price', 'restrictions']
        ].to_dict('list')
        all_requests.append(trade_request_obj)
    if 'send' in args:
        df_all_positions['archive'] = df_all_positions.apply(
            lambda row: TradeRequest(
                created=datetime.utcnow(),
                trade_id=trade.id,
                portfolio_id=row['portfolio_id'],
                account_id=row['account_id'],
                account_number=row['account_number'],
                broker_name=row['broker_name'],
                symbol=row['symbol'],
                shares=row['shares'],
                model_weight=row['model_weight'],
                price=row['price'],
                restrictions=float('NaN')), axis=1)
        db_session.bulk_save_objects(df_all_positions.archive.tolist())
        db_session.commit()
        all_trades = []
        # for t in all_requests:
        #     trade_manager = TradeManager('json', t['portfolio'])
        #     all_trades.append(trade_manager.trade_instructions.to_dict(orient='records'))
        return all_trades
    else:
        return all_requests


def get_iex(trade: Trade):

    current = get_trade_prices(trade)['symbol']
    account_cash = current.loc[current == 'account_cash'].any()
    current = current.loc[current != 'account_cash']

    if current.empty:
        if account_cash:
            return [{'price': 1, 'symbol': 'account_cash'}]
        return []

    batch = Stock(current.tolist())
    prices = batch.get_price()
    if type(prices) == float:
        result = [{'symbol': current.tolist()[0], 'price': prices}]
    else:
        result = [{'price': v, 'symbol': i} for i, v in prices.items()]

    if account_cash:
        result.append({'price': 1, 'symbol': 'account_cash'})

    return result


def prepare_update(trade: Trade, positions: list[AccountPosition]):

    pendings: list[Pending] = trade.pendings
    if not len(pendings):
        current_app.logger.error('You cannot add positions until portfolios have been added to the trade.')
        return (None, None)

    pending_portfolios: list[Portfolio] = [p.portfolio for p in pendings]
    pending_accounts: list[list[Account]] = [a.accounts for a in pending_portfolios]

    pending_details = pd.DataFrame(
        [vars(p) for p in pendings]
    ).set_index(['portfolio_id'])
    pending_account_details = pd.DataFrame(
        [vars(pos) for ap in pending_accounts for pos in ap]
    ).set_index(['portfolio_id'])

    pending_account_details['pending_id'] = pending_details['id']
    pending_account_details.reset_index(inplace=True)

    # check for positions being loaded that are not associated with any account in the trade
    pending_account_details.set_index(['broker_name', 'account_number'], inplace=True)
    new_position_details = pd.DataFrame(positions).groupby(
        ['broker_name', 'account_number', 'symbol']
    ).agg(lambda x: x.astype(float).sum()).reset_index()
    new_account_details = new_position_details.drop_duplicates(
        subset=['broker_name', 'account_number']
    ).set_index(['broker_name', 'account_number'])

    if any(pd.concat([pending_account_details, new_account_details], axis=1)['id'].isna()):
        current_app.logger.error('You have a position that is not associated with any account currently loaded in the trade.')
        return (None, None)

    pending_account_position_details = [vars(ap) for pending in pendings for ap in pending.account_positions]
    new_position_details.set_index(['broker_name', 'account_number'], inplace=True)
    new_position_details = new_position_details.join(
        pending_account_details, on=['broker_name', 'account_number']
    ).reset_index()

    return new_position_details, pending_account_position_details


def create_pending_account_positions(
    trade: Trade, new_positions: pd.DataFrame, pending_positions: pd.DataFrame
):

    if len(pending_positions) == 0:
        additions = new_positions
    else:
        new_positions.set_index(['broker_name', 'account_number', 'symbol'], inplace=True)
        pending_account_position_details = pd.DataFrame(pending_positions).set_index(
            ['broker_name', 'account_number', 'symbol']
        )
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #     print(additions, '\n', pending_account_position_details)
        new_positions['account_position_id'] = pending_account_position_details['id']
        # print(additions.loc[:,['id', 'account_id', 'account_position_id']])
        additions = new_positions[new_positions.loc[:, 'account_position_id'].isna()].reset_index()
    if not additions.empty:
        additions['position'] = additions.apply(
            lambda row: AccountPosition(
                pending_id=row['pending_id'],
                portfolio_id=row['portfolio_id'],
                account_id=row['id'],
                broker_name=row['broker_name'],
                account_number=row['account_number'],
                symbol=row['symbol'],
                shares=row['shares']
            ),
            axis=1
        )

        db_session.bulk_save_objects(additions['position'].tolist())
        db_session.commit()

        additions['price'] = additions.apply(
            lambda row: Price(
                account_position_id=additions['position'].id,
                trade_id=trade.id,
                symbol=row['symbol']
            ),
            axis=1
        )
        db_session.bulk_save_objects(additions['price'].tolist())
        db_session.commit()


def remove_pending_account_positions(new_positions, pending_positions):

    if len(pending_positions) == 0:
        return

    # new_positions.set_index(['broker_name', 'account_number', 'symbol'], inplace=True)
    pending_positions = pd.DataFrame(pending_positions).set_index(
        ['broker_name', 'account_number', 'symbol']
    )
    pending_positions['account_position_id'] = new_positions['id']
    deletions = pending_positions[pending_positions.loc[:, 'account_position_id'].isna()].reset_index()
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(deletions)
    if not deletions.empty:
        db_session.query(Price).filter(
            Price.account_position_id.in_(deletions['id'].tolist())
        ).delete(synchronize_session=False)
        db_session.query(AccountPosition).filter(
            AccountPosition.id.in_(deletions['id'].tolist())
        ).delete(synchronize_session=False)
        db_session.commit()
