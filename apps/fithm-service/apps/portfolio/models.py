from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from libs.database import Base


class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    model_id = Column(Integer, ForeignKey('models.id'))
    name = Column(String)
    business = relationship("Business", back_populates="portfolios")
    accounts = relationship("Account", back_populates="portfolio")
    model = relationship("Model", uselist=False, back_populates="portfolio")
    pendings = relationship(
        "Pending", back_populates="portfolio", cascade="all, delete, delete-orphan")
    account_positions = relationship("AccountPosition", back_populates="portfolio",
                                     cascade="all, delete, delete-orphan")

    def as_dict(self):
        result = {'id': self.id, 'user_id': self.business.user_id, 'name': self.name, 'model': None,
                  'pendings': [], 'accounts': []}
        if self.accounts:
            result['accounts'] = [a.as_dict() for a in self.accounts]
        if self.model:
            result['model'] = self.model.as_dict()
        if self.pendings:
            result['pendings'] = [p.as_dict() for p in self.pendings]
        return result
