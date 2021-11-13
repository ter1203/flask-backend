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


class Pending(Base):
    __tablename__ = 'pendings'
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, ForeignKey('trades.id'))
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    portfolio_name = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))
    trade = relationship("Trade", back_populates="pendings")
    portfolio = relationship("Portfolio", back_populates="pendings")
    account_positions = relationship(
        "AccountPosition", back_populates="pending", cascade="all, delete, delete-orphan")

    def as_dict(self):
        result = {'id': self.id, 'trade_id': self.trade_id, 'portfolio_id': self.portfolio_id, 'account_positions': [],
                  'portfolio_name': 'null'}
        if self.portfolio_name:
            result['portfolio_name'] = self.portfolio_name
        if self.account_positions:
            account_positions = []
            for a in self.account_positions:
                account_positions.append(a.as_dict())
            result['account_positions'] = account_positions
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
