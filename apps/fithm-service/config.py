from settings import (
    LOG_CONFIG,
    FITHM_SMTP_HOST,
    FITHM_SMTP_PORT,
    FITHM_SMTP_USER,
    FITHM_SMTP_PASS,
    FITHM_ADMIN_MAIL,
    FITHM_ADMIN_PASS,
    GATEWAY_SEC_KEY,
    DEBUG
)
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': LOG_CONFIG
})


class Config:
    """General Configuration"""

    # flask mail service
    MAIL_SERVER = FITHM_SMTP_HOST
    MAIL_PORT = FITHM_SMTP_PORT
    MAIL_USERNAME = FITHM_SMTP_USER
    MAIL_PASSWORD = FITHM_SMTP_PASS
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    ADMIN_MAIL_USER = FITHM_ADMIN_MAIL
    ADMIN_MAIL_PASS = FITHM_ADMIN_PASS

    ALLOWED_FILES = ['png', 'jpg', 'jpeg', 'gif']

    SECURITY_KEY = GATEWAY_SEC_KEY
    DEBUG = DEBUG
