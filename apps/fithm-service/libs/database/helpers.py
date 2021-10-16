from flask import current_app
from . import db_session
from apps.models import (
    Pending, Trade, Portfolio, ModelPosition, Price,
    Model, Account
)
import pandas as pd
import numpy


def update_trade_for_portfolio_model(pendings: list[Pending], add: bool = True):

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


def update_pendings_of_trade(trade: Trade, portfolios: list[Portfolio]):
    
    if add_portfolio_pendings(trade, portfolios):
        remove_portfolio_pendings(trade, portfolios)
        add_model_positions_to_price(trade, portfolios)
        remove_model_positions_from_price(trade, portfolios)

        current_app.logger.info(f'Updated trade: {trade}')
    else:
        current_app.logger.info(f'No updates')


def add_portfolio_pendings(trade: Trade, portfolios: list[Portfolio]):

    if not any(portfolio.model_id for portfolio in portfolios):
        no_models = [p.id for p in portfolios if p.model_id == None]
        current_app.logger.info(f'You can\'t add portfolio that hasn\'t been assigned to a model {no_models}')
        return

    trade_pendings: list[Pending] = trade.pendings
    current_pendings = pd.DataFrame([vars(p) for p in trade_pendings])
    portfolio_frames = pd.DataFrame([vars(p) for p in portfolios])
    if current_pendings.empty:
        additions = portfolio_frames
    else:
        additions = portfolio_frames[~portfolio_frames['id'].isin(current_pendings['portfolio_id'])]
    
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


def remove_portfolio_pendings(trade: Trade, portfolios: list[Portfolio]):

    trade_pendings: list[Pending] = trade.pendings
    current_pendings = pd.DataFrame([vars(p) for p in trade_pendings])
    portfolio_frames = pd.DataFrame([vars(p) for p in portfolios])

    if portfolio_frames.empty:
        deletions = current_pendings
    else:
        deletions = current_pendings[~(current_pendings['portfolio_id'].isin(portfolio_frames['id'].tolist()))]

    if not deletions.empty:
        pendings = db_session.query(Pending).filter(Pending.id.in_(deletions['id'].to_list()))
        for pending in pendings:
            db_session.delete(pending)

        db_session.commit()


def add_model_positions_to_price(trade: Trade, portfolios: list[Portfolio]):
    
    models: list[Model] = list(set([portfolio.model for portfolio in portfolios]))
    allocations: list[list[ModelPosition]] = [model.allocation for model in models if hasattr(model, 'allocation')]
    positions = [vars(pos) for allocation in allocations for pos in allocation]
    prices: list[Price] = trade.prices
    prices = list(filter(lambda price: price.model_position_id != None, prices))

    pending_positions = numpy.array([vars(p) for p in prices])
    additions: numpy.ndarray = numpy.array(positions)[
        numpy.isin(
            [a['id'] for a in positions],
            [a['model_position_id'] for a in pending_positions],
            invert=True
        )
    ]

    if additions.size != 0:
        set_model_positions_to_price(trade, additions)


def remove_model_positions_from_price(trade: Trade, portfolios: list[Portfolio]):

    models: list[Model] = list(set([portfolio.model for portfolio in portfolios]))
    allocations: list[list[ModelPosition]] = [model.allocation for model in models if hasattr(model, 'allocation')]
    positions = [vars(pos) for allocation in allocations for pos in allocation]
    prices: list[Price] = trade.prices
    prices = list(filter(lambda price: price.model_position_id != None, prices))

    pending_positions = numpy.array([vars(p) for p in prices])
    deletions: numpy.ndarray = numpy.array(prices)[
        numpy.isin(
            [a['id'] for a in positions],
            [a['model_position_id'] for a in pending_positions],
            invert=True
        )
    ]

    if deletions.size != 0:
        set_model_positions_to_price(trade, deletions)


def set_model_positions_to_price(trade: Trade, positions: list, action: str = 'a'):

    if action == 'a':
        prices = []
        for pos in positions:
            prices.append(Price(
                trade_id=trade.id,
                symbol=pos['symbol'],
                model_position_id=pos['id']
            ))

        db_session.bulk_save_objects(prices)
    else:
        for pos in positions:
            db_session.delete(pos)
    
    db_session.commit()


def update_portfolio_accounts(portfolio: Portfolio, accounts: list[Account]):

    portfolio.accounts = accounts
    db_session.commit()


