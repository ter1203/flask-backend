import os

APP_TITLE = 'fithm'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'prod')

FITHM_USE_SMTP = os.environ.get('FITHM_USE_SMTP') == 'True'
FITHM_SMTP_HOST = os.environ.get('FITHM_SMTP_HOST')
FITHM_SMTP_PORT = os.environ.get('FITHM_SMTP_PORT')
FITHM_SMTP_USER = os.environ.get('FITHM_SMTP_USER')
FITHM_SMTP_PASS = os.environ.get('FITHM_SMTP_PASS')
FITHM_ADMIN_MAIL = os.environ.get('FITHM_ADMIN_MAIL')
FITHM_ADMIN_PASS = os.environ.get('FITHM_ADMIN_PASS')

FITHM_QUOVO_KEY = os.environ.get('FITHM_QUOVO_KEY')
GATEWAY_SEC_KEY = os.environ.get('GATEWAY_SEC_KEY')

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASS = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'fithm')
DEBUG = os.environ.get('DEBUG') == 'True'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(ROOT_DIR, 'storage')
RESOURCES_DIR = os.path.join(STORAGE_DIR, 'resources')

POSTGRES_DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

LOG_CONFIG = { 'level': 'DEBUG' } if DEBUG else { 'level': 'INFO' }

if not FITHM_USE_SMTP:
	FITHM_SMTP_HOST = 'smtp.mailtrap.io'
	FITHM_SMTP_PORT = 2525
	FITHM_SMTP_USER = '19e9588c473008'
	FITHM_SMTP_PASS = '1e9b064e2329d7'
