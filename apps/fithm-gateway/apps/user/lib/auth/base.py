from typing import Dict
import jwt
from flask import current_app, abort, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta
from libs.database import db_session
from apps.user.models import User

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


    def create_confirm_token(self, user_id):
        '''Create confirmation token'''

        sec_key: str = current_app.config['SECRET_KEY']
        expire: int = current_app.config['EXPIRE_TIME']['confirm_token']
        expire_time = datetime.utcnow() + timedelta(minutes=expire)

        return self.__create_token({
            'id': user_id,
            'expired': int(expire_time.timestamp())
        }, f'{sec_key}_conf')


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
        try:
            payload = jwt.decode(token, sec_key, ['HS256'])
            if self.__is_expired(payload):
                abort(401, 'Token expired')

            user = db_session.query(User).filter(User.id == payload['id']).first()
            if user.access != payload['access']:
                abort(401, 'Not a current token')

            return user

        except Exception as ex:
            abort(400, 'Invalid token')


    def confirm_email(self, token: str):
        '''Confirm email using the token'''

        sec_key: str = current_app.config['SECRET_KEY']
        payload = jwt.decode(token, f'{sec_key}_conf', ['HS256'])


    def regen_tokens(self, refresh_token: str):
        '''Re-generate token from the refresh token'''
        pass


    def __create_token(self, body: Dict, sec_key: str) -> str:
        '''Create a token based on body and secret key'''

        return jwt.encode(body, sec_key)


    def __get_authorization_token(self, request: Request):
        authorization = request.headers.get('Authorization')

        if not authorization or not authorization.startswith('Bearer '):
            return None

        token = authorization[7:]
        return token


    def __is_expired(self, payload: Dict):
        '''Check if the token is expired'''

        expired = payload['expired']
        now = datetime.utcnow().timestamp()
        return now > expired
