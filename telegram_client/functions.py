import requests as re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .constants import LOGIN_URL, PROFILE_URL, TOKEN_URL
from .db import ENGINE, TelegramUser


def reverse_choices(choices: tuple) -> tuple:
    return tuple((choice[::-1] for choice in choices))


async def create_token(user_data: dict):
    re.post(LOGIN_URL, data=user_data, timeout=5)
    return re.post(TOKEN_URL, data=user_data, timeout=5).json()['access']


async def compile_header(token: str):
    return {'Authorization': f'Bearer {token}'}


async def backend_get(url: str, token: str) -> re.Response:
    headers = await compile_header(token)
    return re.get(url, headers=headers, timeout=5)


async def backend_post(url: str, token: str, data: dict) -> re.Response:
    headers = await compile_header(token)
    return re.post(url, headers=headers, json=data, timeout=5)


async def patch_profile(token: str, data: dict) -> re.Response:
    headers = await compile_header(token)
    return re.patch(PROFILE_URL, headers=headers, json=data, timeout=5)


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
