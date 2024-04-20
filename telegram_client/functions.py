from aiohttp import ClientResponse, ClientSession
from aiohttp.client import ClientConnectorError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .constants import LOGIN_URL, PROFILE_URL, TOKEN_URL
from .db import ENGINE, TelegramUser


def reverse_choices(choices: tuple) -> tuple:
    return tuple((choice[::-1] for choice in choices))


async def create_token(user_data: dict):
    async with ClientSession() as session:
        await session.post(LOGIN_URL, data=user_data, timeout=5)
        async with session.post(TOKEN_URL, data=user_data, timeout=5) as resp:
            return (await resp.json())['access']


async def compile_header(token: str):
    return {'Authorization': f'Bearer {token}'}


async def backend_get(url: str, token: str) -> ClientResponse | dict:
    headers = await compile_header(token)
    async with ClientSession() as session:
        try:
            return await session.get(url, headers=headers, timeout=5)
        except ClientConnectorError:
            return {'error': 'CONN'}


async def backend_post(
        url: str, token: str, data: dict) -> ClientResponse | dict:
    headers = await compile_header(token)
    async with ClientSession() as session:
        try:
            return await session.post(
                url, headers=headers, json=data, timeout=5)
        except ClientConnectorError:
            return {'error': 'CONN'}


async def backend_delete(url: str, token: str) -> ClientResponse | dict:
    headers = await compile_header(token)
    async with ClientSession() as session:
        try:
            return await session.delete(url, headers=headers, timeout=5)
        except ClientConnectorError:
            return {'error': 'CONN'}


async def patch_profile(token: str, data: dict) -> ClientResponse | dict:
    headers = await compile_header(token)
    async with ClientSession() as session:
        try:
            return await session.patch(
                PROFILE_URL, headers=headers, json=data, timeout=5)
        except ClientConnectorError:
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
