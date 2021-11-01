from flask import g
from libs.database import db_session

from apps.models import User


class UserView:

    def get(self):
        '''Get the user'''

        user: User = g.user
        return user.as_dict()


    def update(self, param: dict):
        '''Update user'''

        user: User = g.user

        for key in param:
            setattr(user, key, param[key])

        db_session.commit()
        return user.as_dict()


    def delete(self):
        '''Delete user'''

        user: User = g.user
        db_session.delete(user)
        db_session.commit()

        return {
            'result': 'success'
        }
