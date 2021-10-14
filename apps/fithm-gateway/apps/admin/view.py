from flask import abort
from libs.database import db_session
from apps.models import User

class AdminView():
    def __init__(self):
        pass


    def get_users(self, page: int, page_size: int) -> list:
        
        total = db_session.query(User).count()
        users = db_session.query(User).offset((page - 1) * page_size).limit(page_size).all()

        return {
            'total': total,
            'users': [user.as_dict() for user in users]
        }