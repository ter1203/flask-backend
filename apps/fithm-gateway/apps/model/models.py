from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Integer,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from libs.database import Base


class Model(Base):
    '''Model table'''

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    name = Column(String)
    description = Column(String)
    keywords = Column("data", postgresql.ARRAY(String))
    is_public = Column(Boolean, default=False, nullable=False)
    business = relationship("Business", back_populates="models")
    allocation = relationship(
        "ModelPosition", back_populates="model", cascade="all, delete, delete-orphan")
    portfolio = relationship("Portfolio", back_populates="model")

    def as_dict(self):
        result = {'id': self.id, 'name': self.name, 'keywords': [], 'positions': None,
                  'is_public': str(self.is_public).lower()}
        if not self.is_public:
            result['user_id'] = self.business.user_id
        if self.allocation:
            result['positions'] = [a.as_dict() for a in self.allocation]
        if self.keywords:
            result['keywords'] = [k for k in self.keywords]
        return result


class ModelPosition(Base):
    __tablename__ = 'model_positions'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'), nullable=False)
    symbol = Column(String)
    weight = Column(Float)
    price = Column(Float)
    model = relationship("Model", back_populates="allocation")
    trade_prices = relationship(
        "Price", back_populates="model_position", cascade="all, delete, delete-orphan")

    def as_dict(self):
        result = {'model_id': self.model_id,
                  'symbol': self.symbol, 'weight': self.weight}
        return result
