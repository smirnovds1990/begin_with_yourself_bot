from os import getenv
from urllib.parse import urljoin

from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'http://127.0.0.1:8000/'
LOGIN_URL = urljoin(BASE_URL, 'auth/users/')
TOKEN_URL = urljoin(BASE_URL, 'auth/jwt/create/')
USER_URL = urljoin(BASE_URL, 'auth/users/me/')
PROFILE_URL = urljoin(BASE_URL, 'profile/')
WORKOUT_URL = urljoin(BASE_URL, 'api/workouts/')
WORKOUT_USER_URL = urljoin(WORKOUT_URL, 'user_workout_program/')
WORKOUT_SESSION_URL = urljoin(WORKOUT_URL, 'workout-session/')

NAMES_PATTERN = r'[А-Яа-я]'
WIGHT_PATTERN = r'^[0-9]{2,3}?\.?[0-9]{0,2}$'
HEIGHT_PATTERN = r'^[0-9]{3,3}$'
DATE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[1-2][0-9]{3}$'
BIRTH_YEAR_PATTERN = r'^[1-2][0-9]{3}$'

MIN_LENGTH = 2
MAX_NAME_LENGTH = 25
MAX_HEIGHT_LENGTH = 3
MAX_WEIGHT_LENGTH = 6
DATE_LENGTH = 10
TOKEN_LENGTH = 256

POSTGRES_TG_USER = getenv('POSTGRES_USER')
POSTGRES_TG_PASSWORD = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
POSTGRES_TG_DB = getenv('POSTGRES_DB')
DATABASE_URL = (
    f'postgresql+asyncpg://{POSTGRES_TG_USER}:{POSTGRES_TG_PASSWORD}@'
    f'{DB_HOST}:{DB_PORT}/{POSTGRES_TG_DB}'
)
YEAR_LENGTH = 4

SEX_CHOICES = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)

ACTIVITY_CHOICES = (
    ('sedentary', 'Сидячий образ жизни 🪑'),
    ('light', 'Тренировки 1-3 раза в неделю 🏃'),
    ('moderate', 'Тренировки 3-5 раз в неделю 🤸'),
    ('intensive', 'Тренировки 6-7 раз в неделю 🏋️‍♀️'),
    ('athlete', 'Тренировки каждый день чаще чем раз в день 🏋️‍♂️'),
)

AIM_CHOICES = (
    ('gain', 'Набор'),
    ('loss', 'Сушка'),
    ('maintain', 'Поддержание'),
)


NOTIFICATIONS = (
    'ОЧЕНЬ ВАЖНО ЗАНИМАТЬСЯ!',
    'НУ ПРАВДА, ПОЗАНИМАЙСЯ УЖЕ!',
    'НЕ ЗАБЫВАЙ СПАТЬ!'
)
