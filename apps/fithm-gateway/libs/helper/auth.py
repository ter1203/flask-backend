from passlib.context import CryptContext


class AuthHelper:
    '''Authentication helper'''

    def __init__(self):
        self.context: CryptContext = CryptContext(
            schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:

        return self.context.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:

        return self.context.verify(password, hashed)
