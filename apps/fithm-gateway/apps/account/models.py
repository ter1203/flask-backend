from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship
from libs.database import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String, primary_key=True)
    business_id = Column(String, ForeignKey('businesses.id'), nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    portfolio_id = Column(String, ForeignKey('portfolios.id'), nullable=True)
    business = relationship("Business", back_populates="accounts")
    portfolio = relationship("Portfolio", back_populates="accounts")
    account_positions = relationship(
        "AccountPosition", back_populates="account", cascade="all, delete, delete-orphan"
    )

    def as_dict(self):
        result = {'id': self.id, 'user_id': self.business.user_id, 'account_number': self.account_number,
                  'broker_name': self.broker_name, 'portfolio_id': 'null'}
        if self.portfolio_id:
            result['portfolio_id'] = self.portfolio_id
        return result


class AccountPosition(Base):
    __tablename__ = 'account_positions'
    id = Column(String, primary_key=True)
    pending_id = Column(String, ForeignKey('pendings.id'), nullable=False)
    portfolio_id = Column(String, ForeignKey('portfolios.id'), nullable=False)
    account_id = Column(String, ForeignKey('accounts.id'), nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    pending = relationship("Pending", back_populates="account_positions")
    account = relationship("Account", back_populates="account_positions")
    portfolio = relationship("Portfolio", back_populates="account_positions")
    trade_prices = relationship(
        "Price", back_populates="account_position", cascade="all, delete, delete-orphan")

    def as_dict(self):
        return (
            {'id': self.id, 'pending_id': self.pending_id, 'portfolio_id': self.portfolio_id, 'account_id': self.account_id,
             'broker_name': self.broker_name, 'account_number': self.account_number, 'symbol': self.symbol,
             'shares': str(self.shares)})
