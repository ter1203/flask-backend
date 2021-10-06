from libs.database import db_session
from .models import User

from libs.depends.entry import container
from libs.helper.auth import AuthHelper


class UserView:
    
    def __init__(self):
        # self.auth_helper: AuthHelper = container.get(AuthHelper)
        self.auth_helper = None


    def signup(self, param: dict):
        '''Create a new user'''

        email = param['email']
        username = param['username']
        password = param['password']

        user = User(
            email=email,
            username=username,
            password=self.auth_helper.hash_password(password)
        )
        db_session.add(user)
        db_session.commit()

        return user
