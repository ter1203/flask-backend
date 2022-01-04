from apps.models import Portfolio
from libs.database import db_session


def get_portfolios(ids: list[int]) -> list[Portfolio]:

    return db_session.query(Portfolio).filter(Portfolio.id.in_(ids)).all()
