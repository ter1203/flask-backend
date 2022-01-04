import re
from flask import current_app

def email_is_valid(email: str) -> bool:
    return re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None


def password_is_valid(password: str) -> bool:
    if len(password) < current_app.config['PASSWORD_MIN_LENGTH']:
        return False

    return True
