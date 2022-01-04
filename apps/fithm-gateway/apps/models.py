from apps.auth.models import User, Role, RolesUsers
from apps.account.models import Account, AccountPosition
from apps.model.models import Model, ModelPosition
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade, TradeRequest

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Integer
)
from sqlalchemy.orm import relationship
from libs.database import Base

class Business(Base):
    '''User business'''

    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    models = relationship("Model", back_populates="business",
                          cascade="all, delete, delete-orphan")
    portfolios = relationship(
        "Portfolio", back_populates="business", cascade="all, delete, delete-orphan")
    trades = relationship("Trade", back_populates="business",
                          cascade="all, delete, delete-orphan")
    accounts = relationship(
        "Account", back_populates="business", cascade="all, delete, delete-orphan")
    user = relationship('User', back_populates='business', single_parent=True,
                        cascade="all, delete, delete-orphan")

    def as_dict(self):
        return ({'id': self.id, 'user_id': self.user_id})


class TradePortfolio(Base):
    __tablename__ = 'trade_portfolios'
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, ForeignKey('trades.id'))
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    trade = relationship("Trade", back_populates="portfolios")
    portfolio = relationship("Portfolio", back_populates="trades")

    def as_dict(self):
        result = {'id': self.id, 'trade_id': self.trade_id, 'portfolio_id': self.portfolio_id}
        return result


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    account_position_id = Column(Integer, ForeignKey('account_positions.id'))
    model_position_id = Column(Integer, ForeignKey('model_positions.id'))
    trade_id = Column(Integer, ForeignKey('trades.id'))
    symbol = Column(String, nullable=False)
    price = Column(Float)
    trade = relationship("Trade", back_populates="prices")
    model_position = relationship(
        "ModelPosition", back_populates="trade_prices")
    account_position = relationship(
        "AccountPosition", back_populates="trade_prices")

    def as_dict(self):
        return {'id': self.id, 'trade_id': self.trade_id, 'symbol': self.symbol, 'price': str(self.price)}
