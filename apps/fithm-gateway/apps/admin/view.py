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


    def get_user(self, id: int) -> dict:

        user = self.__get_user(id)
        return user.as_dict()


    def update_user(self, id: int, body: dict) -> dict:

        user = self.__get_user(id)
        for key in body:
            if hasattr(user, key):
                setattr(user, key, body[key])

        db_session.commit()
        return self.__get_user(id)


    def delete_user(self, id: int):
        
        user = self.__get_user(id)
        db_session.delete(user)

        return {
            'result': 'success'
        }


    def __get_user(self, id: int) -> User:

        user = db_session.query(User).get(id)
        if not user:
            abort(404, 'User not found')

        return user
