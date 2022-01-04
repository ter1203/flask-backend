from typing import Dict
import jwt
from flask import current_app, abort, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta
from libs.database import db_session
from apps.auth.models import User

class AuthBase:
    '''Authentication helper'''

    def __init__(self):
        self.context: CryptContext = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )


    def hash_password(self, password: str) -> str:

        return self.context.hash(password)


    def verify_password(self, password: str, hashed: str) -> bool:

        return self.context.verify(password, hashed)


    def create_confirm_token(self, user_id: str) -> str:
        '''Create confirmation token'''

        sec_key: str = current_app.config['SECRET_KEY']
        expire: int = current_app.config['EXPIRE_TIME']['confirm_token']
        expire_time = datetime.utcnow() + timedelta(minutes=expire)

        return self.__create_token({
            'id': user_id,
            'expired': int(expire_time.timestamp())
        }, f'{sec_key}_conf')


    def create_reset_token(self, user_id: str) -> str:
        '''Create reset-password token'''

        sec_key: str = current_app.config['SECRET_KEY']
        expire: int = current_app.config['EXPIRE_TIME']['reset_token']
        expire_time = datetime.utcnow() + timedelta(minutes=expire)

        return self.__create_token({
            'id': user_id,
            'expired': int(expire_time.timestamp())
        }, f'{sec_key}_reset')


    def get_user_from_reset(self, reset_token: str) -> str:

        sec_key: str = current_app.config['SECRET_KEY']
        (user_id, payload) = self.__get_user_from_token(reset_token, f'{sec_key}_reset')

        return user_id


    def create_tokens(self, user_id: int, access: str) -> Dict:
        '''Create access token and refresh token'''

        sec_key: str = current_app.config['SECRET_KEY']

        expire: int = current_app.config['EXPIRE_TIME']['access_token']
        expire_time = datetime.utcnow() + timedelta(minutes=expire)
        access_token = self.__create_token({
            'id': user_id,
            'access': access,
            'expired': int(expire_time.timestamp())
        }, sec_key)

        expire = current_app.config['EXPIRE_TIME']['refresh_token']
        expire_time = datetime.utcnow() + timedelta(minutes=expire)
        refresh_token = self.__create_token({
            'id': user_id,
            'expired': int(expire_time.timestamp())
        }, f'{sec_key}_ref')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }


    def get_user_from_authorization(self, request: Request):
        '''Get user from Authorization header'''

        token = self.__get_authorization_token(request)
        if not token:
            return None

        sec_key: str = current_app.config['SECRET_KEY']
        (user_id, payload) = self.__get_user_from_token(token, sec_key)

        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, 'User not found')

        if 'access' not in payload:
            abort(400, 'Invalid token')

        if user.access != payload['access']:
            abort(401, 'Not a current token')

        return user


    def confirm_email(self, token: str):
        '''Confirm email using the token'''

        sec_key: str = current_app.config['SECRET_KEY']
        try:
            payload = jwt.decode(token, f'{sec_key}_conf', ['HS256'])
        except Exception as e:
            abort(400, 'Invalid token')

        current_app.logger.debug(f'confirm_email with token {payload}')
        if self.__is_expired(payload):
            abort(400, 'Expired token')

        user = db_session.query(User).filter(User.id == payload['id']).first()
        if not user:
            abort(404, 'Not found')

        user.active = True
        db_session.commit()


    def get_user_from_refresh(self, refresh_token: str):
        '''Re-generate token from the refresh token'''
        
        sec_key: str = current_app.config['SECRET_KEY']
        (user_id, payload) = self.__get_user_from_token(refresh_token, f'{sec_key}_ref')

        return user_id


    def __create_token(self, body: Dict, sec_key: str) -> str:
        '''Create a token based on body and secret key'''

        return jwt.encode(body, sec_key, 'HS256')


    def __get_authorization_token(self, request: Request):
        authorization = request.headers.get('Authorization')

        if not authorization or not authorization.startswith('Bearer '):
            return None

        token = authorization[7:]
        return token


    def __get_user_from_token(self, token: str, sec_key: str) -> tuple:
        '''Get user from token'''

        payload = jwt.decode(token, sec_key, ['HS256'])
        if self.__is_expired(payload):
            abort(401, 'Token expired')

        return (payload['id'], payload)


    def __is_expired(self, payload: Dict):
        '''Check if the token is expired'''

        expired = payload['expired']
        now = datetime.utcnow().timestamp()
        return now > expired
