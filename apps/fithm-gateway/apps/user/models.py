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
from libs.database import Base


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
    business_id = Column(String, ForeignKey('businesses.id'), nullable=False)
    business = relationship('Business', back_populates='user')
    roles = relationship(
        'Role', secondary='roles_users',
        backref=backref('users', lazy='dynamic')
    )


class ApiKey(Base):
    __tablename__ = 'keys'
    api_key = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="user_api_key")

    def as_dict(self):
        return ({'api_key': self.api_key, 'user_id': self.user_id})
