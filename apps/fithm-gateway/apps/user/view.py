from flask import g, current_app, abort
from libs.database import db_session
from libs.depends.entry import container
from apps.auth.lib.auth.authenticator import Authenticator

from apps.models import User


class UserView:

    def __init__(self):
        self.authenticator: Authenticator = container.get(Authenticator)


    def get(self):
        '''Get the user'''

        user: User = g.user
        return user.as_dict()


    def update(self, param: dict):
        '''Update user'''

        user: User = g.user
        password = None

        current_app.logger.debug(f'params: {param}, {user.password}')
        if 'old_password' in param and param['old_password']:
            if not self.authenticator.verify_password(param['old_password'], user.password):
                current_app.logger.debug('password is incorrect')
                abort(401, 'password is incorrect')

            password = param['new_password']
            del param['old_password']
            del param['new_password']

        for key in param:
            setattr(user, key, param[key])

        if password is not None:
            user.password = self.authenticator.hash_password(password)

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
