from datetime import datetime
from uuid import uuid4
from flask import abort, request, g
from flask_mail import Message
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
        user.access = str(uuid4())
        db_session.commit()

        return self.authenticator.create_tokens(user.id, user.access)


    def signout(self):
        '''Sign out'''

        user: User = g.user
        user.access = ''
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = request.remote_addr
        db_session.commit()

        return {
            'last_login': user.last_login_at.isoformat()
        }


    def confirm(self, token: str):
        '''Confirm email'''

        self.authenticator.confirm_email(token)
        return {
            'result': 'success'
        }


    def send_confirm(self):
        user: User = g.user
        token = self.authenticator.create_confirm_token(user.id)
        
        return token
