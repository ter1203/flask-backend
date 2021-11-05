from datetime import datetime
from uuid import uuid4
from flask import abort, request, g, current_app
from libs.email.message import make_mail, send_msg
from libs.database import db_session
from libs.depends.entry import container
from .lib.auth.authenticator import Authenticator
from apps.models import User, Business
from threading import Thread


class AuthView:

    def __init__(self):
        self.authenticator: Authenticator = container.get(Authenticator)


    def signup(self, param: dict):
        '''Create a new user'''

        current_app.logger.debug('signup')
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

        current_app.logger.debug(f'user: {user}')
        db_session.add(user)
        business = Business(user=user)
        db_session.add(business)
        db_session.commit()

        msg = self.__make_confirm_mail(user)
        def post_request():
            send_msg(msg)
        Thread(target=post_request).start()

        return user.as_dict()


    def delete(self):
        '''Delete user'''

        user: User = g.user
        db_session.delete(user)
        db_session.commit()

        return { 'result': 'success' }


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

        return {
            'user': user.as_dict(),
            'tokens': self.authenticator.create_tokens(user.id, user.access)
        }


    def signout(self):
        '''Sign out'''

        user: User = g.user
        user.access = ''
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = request.remote_addr
        db_session.commit()

        return { 'last_login': user.last_login_at.isoformat() }


    def confirm(self, token: str):
        '''Confirm email'''

        self.authenticator.confirm_email(token)
        return { 'result': 'success' }


    def send_confirm(self):
        '''Send confirm email'''

        msg = self.__make_confirm_mail(g.user)
        send_msg(msg)

        return { 'result': 'success' }


    def forgot_password(self, email: str):

        user = db_session.query(User).filter(User.email == email).first()
        if not user:
            abort(404, 'User not found')

        reset_token = self.authenticator.create_reset_token(user.id)

        msg = make_mail(
            'Reset your password',
            current_app.config['ADMIN_MAIL_USER'],
            [user.email],
            'reset_password.html',
            app_title='fithm.com',
            link=reset_token
        )

        send_msg(msg)

        return { 'result': 'success' }


    def reset_password(self, reset_token: str, password: str):

        user_id = self.authenticator.get_user_from_reset(reset_token)
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, 'User not found')

        user.password = self.authenticator.hash_password(password)
        db_session.commit()

        return { 'result': 'success' }


    def __make_confirm_mail(self, user: User):
        '''Send confirm email'''

        token = self.authenticator.create_confirm_token(user.id)
        base = current_app.config['BASE_URL']
        return make_mail(
            'Confirm your email',
            current_app.config['ADMIN_MAIL_USER'],
            [user.email],
            'email_confirm.html',
            app_title='fithm.com',
            link=f'{base}/auth/confirm?confirm_token={token}'
        )
