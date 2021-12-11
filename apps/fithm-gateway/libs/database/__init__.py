from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean
from settings import POSTGRES_DB_URL

engine = create_engine(
    POSTGRES_DB_URL,
    convert_unicode=True,
    max_overflow=100
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

class Stateful(Base):
    __abstract__ = True
    active = Column(Boolean(), nullable=False, default=True)


def init_db(app: Flask):
    """Initialize the database and flask app"""

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()


def create_tables():
    import apps.models
    Base.metadata.create_all(bind=engine)


def populate_default():
    from .defaults import default_values
    default_values()


def drop_tables():
    import apps.models
    Base.metadata.drop_all(bind=engine)

