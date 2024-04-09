import requests as re

from constants import LOGIN_URL, TOKEN_URL


async def get_token(user_data: dict):
    re.post(LOGIN_URL, data=user_data)
    return re.post(TOKEN_URL, data=user_data).json()['access']


async def compile_registration_data(data: dict) -> dict:
    '''
    Функция, обрабатывающая `data` из формы регистрации.
    '''
    data['height'] = int(data['height'])
    data['birth_year'] = int(data['birth_year'])
    return data
