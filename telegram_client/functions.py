import requests as re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .constants import (
    LAST_SLEEP_URL,
    LOGIN_URL,
    PROFILE_URL,
    SLEEP_URL,
    TOKEN_URL,
)
from .db import ENGINE, TelegramUser


def reverse_choices(choices: tuple) -> tuple:
    return tuple((choice[::-1] for choice in choices))


async def create_token(user_data: dict):
    re.post(LOGIN_URL, data=user_data, timeout=5)
    return re.post(TOKEN_URL, data=user_data, timeout=5).json()['access']


async def compile_header(token: str):
    return {'Authorization': f'Bearer {token}'}


async def backend_get(url: str, token: str) -> re.Response | dict:
    headers = await compile_header(token)
    try:
        return re.get(url, headers=headers, timeout=5)
    except re.exceptions.ConnectionError:
        return {'error': 'CONN'}


async def backend_post(url: str, token: str, data: dict) -> re.Response | dict:
    headers = await compile_header(token)
    try:
        return re.post(url, headers=headers, json=data, timeout=5)
    except re.exceptions.ConnectionError:
        return {'error': 'CONN'}


async def patch_profile(token: str, data: dict) -> re.Response | dict:
    headers = await compile_header(token)
    try:
        return re.patch(PROFILE_URL, headers=headers, json=data, timeout=5)
    except re.exceptions.ConnectionError:
        return {'error': 'CONN'}


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


async def create_sleep(user_id: int, is_sleeping: bool = True):
    """Функция, отправляющая запрос на создание сна."""
    return re.post(
        SLEEP_URL,
        headers={'Authorization': f'Bearer {await get_token(user_id)}'},
        data={'is_sleeping': is_sleeping},
        timeout=5,
    )


async def get_last_sleep(user_id: int):
    """Функция, отправляющая запрос на получение информации о последнем сне."""
    return re.get(
        LAST_SLEEP_URL,
        headers={'Authorization': f'Bearer {await get_token(user_id)}'},
        timeout=5,
    ).json()
