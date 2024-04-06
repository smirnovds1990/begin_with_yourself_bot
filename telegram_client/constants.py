from os import getenv

from dotenv import load_dotenv


load_dotenv()

NAMES_PATTERN = r'[А-Яа-я]'
WIGHT_PATTERN = r'^[0-9]{2,3}?\.?[0-9]{0,2}$'
HEIGHT_PATTERN = r'^[0-9]{3,3}$'
DATE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[1-2][0-9]{3}$'

MIN_LENGTH = 2
MAX_NAME_LENGTH = 25
MAX_WEIGHT_LENGTH = 3
MAX_HEIGHT_LENGTH = 5
DATE_LENGTH = 10
TOKEN_LENGTH = 100

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
POSTGRES_DB = getenv('POSTGRES_DB')
DATABASE_URL = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'
)
