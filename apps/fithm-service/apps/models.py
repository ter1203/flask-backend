from sqlalchemy import (
	Column,
	String,
	ForeignKey,
	Float
)
from sqlalchemy.orm import relationship
from libs.database import Base

from apps.account.models import Account, AccountPosition
from apps.model.models import Model, ModelPosition
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade, TradeRequest

class Business(Base):
	'''User business'''

	__tablename__ = 'businesses'

	id = Column(String, primary_key=True)
	user_id = Column(String, ForeignKey('users.id'))
	user_api_key = relationship("Key", uselist=False, back_populates="business", cascade="all, delete, delete-orphan")
	models = relationship("Model", back_populates="business", cascade="all, delete, delete-orphan")
	portfolios = relationship("Portfolio", back_populates="business", cascade="all, delete, delete-orphan")
	trades = relationship("Trade", back_populates="business", cascade="all, delete, delete-orphan")
	accounts = relationship("Account", back_populates="business", cascade="all, delete, delete-orphan")
	user = relationship('User', back_populates='business', cascade="all, delete, delete-orphan")

	def as_dict(self):
		if self.user_api_key:
			return {'id': self.id, 'key': self.user_api_key.as_dict()}
		return ({'id': self.id, 'key': None})


class Pending(Base):
    __tablename__ = 'pendings'
    id = Column(String, primary_key=True)
    trade_id = Column(String, ForeignKey('trades.id'))
    portfolio_id = Column(String, ForeignKey('portfolios.id'), nullable=False)
    portfolio_name = Column(String)
    model_id = Column(String)
    trade = relationship("Trade", back_populates="pendings")
    portfolio = relationship("Portfolio", back_populates="pendings")
    account_positions = relationship("AccountPosition", back_populates="pending", cascade="all, delete, delete-orphan")

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
    id = Column(String, primary_key=True)
    account_position_id = Column(String, ForeignKey('account_positions.id'))
    model_position_id = Column(String, ForeignKey('model_positions.id'))
    trade_id = Column(String, ForeignKey('trades.id'))
    symbol = Column(String, nullable=False)
    price = Column(Float)
    trade = relationship("Trade", back_populates="prices")
    model_position = relationship("ModelPosition", back_populates="trade_prices")
    account_position = relationship("AccountPosition", back_populates="trade_prices")

    def as_dict(self):
        return {'id': self.id, 'trade_id': self.trade_id, 'symbol': self.symbol, 'price': str(self.price)}


from libs.database import Base
from sqlalchemy import (
	Boolean,
	DateTime,
	Column,
	Integer,
	String,
	ForeignKey,
	Enum
)
from sqlalchemy.orm import relationship, backref


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
	business_id = Column(String, ForeignKey('business.id'), nullable=False)
	business = relationship('Business', back_populates='user')
	roles = relationship(
		'Role', secondary='roles_users',
		backref=backref('users', lazy='dynamic')
	)


class ApiKey(Base):
	__tablename__ = 'keys'
	api_key = Column(String, primary_key=True)
	user_id = Column(String, ForeignKey('users.id'), nullable=False)
	user = relationship("User", back_populates="user_api_key")

	def as_dict(self):
		return ({'api_key': self.api_key, 'user_id': self.user_id})
