from datetime import datetime
from flask import abort, request
from libs.database import db_session
from libs.depends.entry import container
from .lib.auth.authenticator import Authenticator

from apps.models import User, Business


class UserView:
    
    def __init__(self):
        self.authenticator: Authenticator = container.get(Authenticator)


    def signup(self, param: dict):
        '''Create a new user'''

        email = param['email']
        username = param['username']
        password = param['password']

        user = db_session.query(User).filter(User.email == email).first()
        if user is not None:
            abort(403, 'Email already exists')

        user = User(
            email=email,
            username=username,
            password=self.authenticator.hash_password(password),
            active=False
        )

        db_session.add(user)
        business = Business(user=user)
        db_session.add(business)
        db_session.commit()

        return user.as_dict()


    def signin(self, email: str, password: str):
        '''Sign in with email'''

        user = db_session.query(User).filter(User.email == email).first()
        if not user:
            abort(404, 'User not found')

        if not self.authenticator.verify_password(password, user.password):
            abort(403, 'Wrong password')

        user.current_login_at = datetime.utcnow()
        user.current_login_ip = request.remote_addr
        user.login_count = (user.login_count or 0) + 1
        db_session.commit()

        return self.authenticator.create_tokens(user.id)
