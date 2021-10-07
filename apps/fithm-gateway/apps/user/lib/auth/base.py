from flask import current_app
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Dict
import jwt


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


    def create_tokens(self, user_id: int) -> Dict:
        '''Create access token and refresh token'''

        sec_key: str = current_app.config['SECURITY_KEY']

        expire: int = current_app.config['LIFE_TIME']['access_token']
        access_token = self.__create_token({
            'id': user_id,
            'expired': datetime.utcnow() + timedelta(minutes=expire)
        }, sec_key)

        expire = current_app.config['LIFE_TIME']['refresh_token']
        refresh_token = self.__create_token({
            'id': user_id,
            'expired': datetime.utcnow() + timedelta(minutes=expire)
        }, sec_key)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }


    def __create_token(self, body: Dict, sec_key: str) -> str:
        '''Create a token based on body and secret key'''

        return jwt.encode(body, sec_key)
