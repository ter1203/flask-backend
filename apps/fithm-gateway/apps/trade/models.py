from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Boolean,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship
from libs.database import Base, Stateful


class Trade(Stateful):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    created = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False)
    business = relationship("Business", back_populates="trades")
    portfolios = relationship("TradePortfolio", back_populates="trade",
                            cascade="all, delete, delete-orphan")
    prices = relationship("Price", back_populates="trade",
                          cascade="all, delete, delete-orphan")

    def as_dict(self):
        result = {'id': self.id, 'name': self.name, 'user_id': self.business.user_id,
                  'created': str(self.created), 'status': str(self.status), 'portfolios': [], 'prices': []}
        if self.portfolios:
            result['portfolios'] = [p.as_dict() for p in self.portfolios]
        if self.prices:
            result['prices'] = [p.as_dict() for p in self.prices]
        return result


class TradeRequest(Base):
    __tablename__ = 'trade_requests'
    id = Column(Integer, primary_key=True)
    created = created = Column(DateTime, nullable=False)
    trade_id = Column(Integer, nullable=False)
    portfolio_id = Column(Integer, nullable=False)
    account_id = Column(Integer, nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    model_weight = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    restrictions = Column(String, nullable=False)
