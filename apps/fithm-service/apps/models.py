from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Integer,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from libs.database import Base

from apps.account.models import Account, AccountPosition
from apps.model.models import Model, ModelPosition
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade, TradeRequest


class RolesUsers(Base):
    '''M-to-M relation between roles and users'''

    __tablename__ = 'roles_users'

    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))


class Role(Base):

    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base):
    '''User table'''

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    access = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    quovo_user_id = Column(String)
    tradeshop_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    phone_number = Column(String)
    business = relationship('Business', back_populates='user', uselist=False)
    roles = relationship(
        'Role', secondary='roles_users',
        backref=backref('users', lazy='dynamic')
    )

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'company': self.company,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
        }


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
