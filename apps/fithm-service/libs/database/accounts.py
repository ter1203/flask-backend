from apps.models import Account, AccountPosition, Portfolio
from libs.database import db_session


def get_accounts(ids: list[int]) -> list[Account]:
    
    return db_session.query(Account).filter(Account.id.in_(ids)).all()


def get_account_positions(ids: list[int]) -> list[AccountPosition]:

    return db_session.query(AccountPosition).filter(AccountPosition.id.in_(ids)).all()
