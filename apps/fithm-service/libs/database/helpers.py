from flask import current_app
from . import db_session
from apps.models import (
    Pending, Trade, Portfolio, ModelPosition, Price,
    Model, Account
)
import pandas as pd

def update_trades_for_pendings(pendings: list[Pending], add: bool = True):
    '''Update trades for pendings'''

    trades: list[Trade] = [pending.trade for pending in pendings]
    for trade in trades:
        trade_pendings: list[Pending] = trade.pendings
        portfolios = [item.portfolio for item in trade_pendings]

        if add:
            add_model_positions_to_price(trade, portfolios)
        remove_model_positions_from_price(trade, portfolios)


def update_trade_for_portfolio_account(portfolio: Portfolio, pendings: list[Pending]):

    trades: list[Trade] = [pending.trade for pending in pendings]
    for trade in trades:
        trade_pendings: list[Pending] = trade.pendings
        portfolios: list[Portfolio] = [item.portfolio for item in trade_pendings]
        portfolios.remove(portfolio)

        trade_update_portfolios(trade, portfolios)


def trade_update_portfolios(trade: Trade, portfolios: list[Portfolio]):

    if not add_portfolio_pendings(trade, portfolios):
        current_app.logger.info(f'No updates')
        return

    remove_portfolio_pendings(trade, portfolios)
    add_model_positions_to_price(trade, portfolios)
    remove_model_positions_from_price(trade, portfolios)

    current_app.logger.info(f'Updated trade: {trade}')


def add_portfolio_pendings(trade: Trade, portfolios: list[Portfolio]) -> bool:
    '''Add new pendings from portfolios that are not in current pendings'''

    if not any(portfolio.model_id for portfolio in portfolios):
        no_models = [
            portfolio.id for portfolio in portfolios if portfolio.model_id == None]
        current_app.logger.info(
            f'You can\'t add portfolio that hasn\'t been assigned to models: {no_models}'
        )
        return False

    trade_pendings: list[Pending] = trade.pendings
    current_pendings = pd.DataFrame([vars(p) for p in trade_pendings])
    portfolio_frames = pd.DataFrame([vars(p) for p in portfolios])
    if current_pendings.empty:
        additions = portfolio_frames
    else:
        additions = portfolio_frames[~portfolio_frames['id'].isin(
            current_pendings['portfolio_id'])]

    if not additions.empty:
        new_pendings = additions.apply(
            lambda row: Pending(
                portfolio_name=row['name'],
                portfolio_id=row['id'],
                model_id=row['model_id'],
                trade_id=trade.id
            )
        )

        db_session.bulk_save_objects(new_pendings.to_list())
        db_session.commit()

        current_app.logger.info(f'New pendings were created')

    return True


def remove_portfolio_pendings(trade: Trade, portfolios: list[Portfolio]):
    '''Remove all pendings from current that are not in portfolios'''

    trade_pendings: list[Pending] = trade.pendings
    current_pendings = pd.DataFrame([vars(p) for p in trade_pendings])
    portfolio_frames = pd.DataFrame([vars(p) for p in portfolios])

    if portfolio_frames.empty:
        deletions = current_pendings
    else:
        deletions = current_pendings[~(
            current_pendings['portfolio_id'].isin(portfolio_frames['id'].tolist()))]

    if not deletions.empty:
        pendings = db_session.query(Pending).filter(
            Pending.id.in_(deletions['id'].to_list()))
        for pending in pendings:
            db_session.delete(pending)

        db_session.commit()


def add_model_positions_to_price(trade: Trade, portfolios: list[Portfolio]):
    '''Add model positions from portfolios to trade that are not in current positions

    new-model-positions: portfolio -> model -> model-position
    current-positions: trade -> prices -> model-position
    '''

    # new positions from portfolios
    models: list[Model] = list(
        set([portfolio.model for portfolio in portfolios]))
    allocations: list[list[ModelPosition]] = [
        model.allocation for model in models if hasattr(model, 'allocation')
    ]
    new_positions = [pos for allocation in allocations for pos in allocation]

    # current positions from prices of trade
    pending_prices: list[Price] = trade.prices
    pending_position_ids = [
        p.model_position_id for p in pending_prices
        if p.model_position_id != None
    ]

    # add
    positions_to_add = [
        p for p in new_positions if p.id not in pending_position_ids
    ]
    prices_to_add = [
        Price(trade_id=trade.id, symbol=pos.symbol, model_position_id=pos.id)
        for pos in positions_to_add
    ]
    db_session.bulk_save_objects(prices_to_add)
    db_session.commit()

    # pending_positions = numpy.array([vars(p) for p in prices])
    # additions: numpy.ndarray = numpy.array(new_positions)[
    #     numpy.isin(
    #         [a['id'] for a in new_positions],
    #         [a['model_position_id'] for a in pending_positions],
    #         invert=True
    #     )
    # ]

    # if additions.size != 0:
    #     set_model_positions_to_price(trade, additions)


def remove_model_positions_from_price(trade: Trade, portfolios: list[Portfolio]):
    '''Remove model positions from trade that are not in new positions from portfolios

    new-model-positions: portfolio -> model -> model-position
    current-positions: trade -> prices -> model-position
    '''

    # new positions from portfolios
    models: list[Model] = list(
        set([portfolio.model for portfolio in portfolios]))
    allocations: list[list[ModelPosition]] = [
        model.allocation for model in models if hasattr(model, 'allocation')
    ]
    new_positions_ids = [
        pos.id for allocation in allocations for pos in allocation]

    # current prices of trade
    pending_prices: list[Price] = [
        p for p in trade.prices if p.model_position_id != None
    ]

    # delete
    prices_to_delete = [
        p for p in pending_prices if p.model_position_id not in new_positions_ids
    ]
    db_session.delete(prices_to_delete)
    db_session.commit()

    # new_positions = [pos for allocation in allocations for pos in allocation]
    # allocations: list[list[ModelPosition]] = [model.allocation for model in models if hasattr(model, 'allocation')]
    # positions = [vars(pos) for allocation in allocations for pos in allocation]
    # prices: list[Price] = trade.prices
    # prices = list(filter(lambda price: price.model_position_id != None, prices))

    # pending_positions = numpy.array([vars(p) for p in prices])
    # deletions: numpy.ndarray = numpy.array(prices)[
    #     numpy.isin(
    #         [a['id'] for a in positions],
    #         [a['model_position_id'] for a in pending_positions],
    #         invert=True
    #     )
    # ]

    # if deletions.size != 0:
    #     set_model_positions_to_price(trade, deletions)


def update_portfolio_accounts(portfolio: Portfolio, accounts: list[Account]):

    portfolio.accounts = accounts
    db_session.commit()
