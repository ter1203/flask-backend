from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

def init_db(app: Flask):
    """Initialize the database and flask app"""

    import apps.models
    Base.metadata.create_all(bind=engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
