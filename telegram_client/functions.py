import requests as re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .constants import LOGIN_URL, PROFILE_URL, TOKEN_URL
from .db import ENGINE, TelegramUser


def reverse_choices(choices: tuple) -> tuple:
    return [choice[::-1] for choice in choices]


async def create_token(user_data: dict):
    re.post(LOGIN_URL, data=user_data, timeout=5)
    return re.post(TOKEN_URL, data=user_data, timeout=5).json()['access']


async def get_profile(token: str):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return re.get(PROFILE_URL, headers=headers, timeout=5).json()


async def get_token(user_id: int):
    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    async with async_session() as session:
        user = (
            await session.scalars(
                select(TelegramUser).where(
                    TelegramUser.tg_user_id == user_id))
                ).one_or_none()
    return user.token


async def compile_registration_data(data: dict) -> dict:
    '''
    Функция, обрабатывающая `data` из формы регистрации.
    '''
    data['height'] = int(data['height'])
    data['birthdate'] = int(data['birthdate'])
    return data
