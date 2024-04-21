import asyncio
from hashlib import sha256
from http import HTTPStatus
from random import choice

from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
from aiogram_forms import FormsManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from telegram_client.config import BOT, DISPATCHER, get_keyboard
from telegram_client.constants import NOTIFICATIONS, PROFILE_URL
from telegram_client.db import ENGINE, TelegramUser
from telegram_client.functions import (
    backend_get,
    create_token,
    get_token,
    create_sleep,
    get_last_sleep,
)


@DISPATCHER.message(Command('start'))
async def start_message(message: Message):
    row = {
        'username': f'{message.from_user.id}',
        'password': sha256(f'{message.from_user.id}'.encode()).hexdigest()
    }
    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    query = select(TelegramUser).where(
        TelegramUser.tg_user_id == message.from_user.id)
    async with async_session() as session:
        if not (await session.scalars(query)).one_or_none():
            row['token'] = await create_token(row)
            row['tg_user_id'] = message.from_user.id
            session.add(TelegramUser(**row))
            await session.commit()
            await message.answer(
                'Приветствую! Вы прошли начальную регистрацию.\n'
                'Здесь должно быть большое описание, '
                'но пока в процессе разработки 😏\n'
                'Зарегистроваться: /register'
            )
        else:
            await message.answer(
                'Вы уже прошли начальную регистрацию 😏\n'
                'Продолжить: /register')


@DISPATCHER.callback_query(F.data == '/nutrition')
async def nutrilon_handler(callback: CallbackQuery):
    await callback.message.answer('/nutrition handler message.')


@DISPATCHER.callback_query(F.data == '/sleep')
async def sleep_handler(callback: CallbackQuery):
    await callback.message.answer('/sleep handler message.')


@DISPATCHER.callback_query(F.data == '/workout')
async def workout_handler(callback: CallbackQuery):
    await callback.message.answer('/workout handler message.')


@DISPATCHER.callback_query(F.data == '/renew')
async def renew_handler(callback: CallbackQuery):
    await callback.message.answer(
        'Для обновления ваших данных вызовите \n/renew 😏')


@DISPATCHER.message(Command('renew'))
async def command_renew(message: Message, forms: FormsManager):
    await message.answer('Давайте зафиксируем ваши данные.')
    await forms.show('training')


@DISPATCHER.message(Command('register'))
async def command_register(message: Message, forms: FormsManager):
    user_token = await get_token(message.from_user.id)
    status = await backend_get(PROFILE_URL, user_token)
    if not isinstance(status, dict):
        if status.status_code == HTTPStatus.OK:
            await message.answer(
                'Вы уже зарегистированы. '
                'Вероятно, кнопки ниже могут вам помочь 🤫',
                reply_markup=get_keyboard())
        elif status.status_code == HTTPStatus.NOT_FOUND:
            await message.answer('Давайте зарегиструемся!')
            await forms.show('registration')
        else:
            await message.answer(
                'Кажется, что-то пошло не так.\n'
                'Попробуйте еще раз или подойдите позже.')
    else:
        await message.answer(
            'Кажется, что-то пошло не так.\n'
            'Попробуйте еще раз или подойдите позже.')


@DISPATCHER.message(Command('sleep'))
async def start_sleep(message: Message):
    """Обработчик события /sleep."""
    await create_sleep(message.from_user.id)
    await message.answer("Приятных снов!")


@DISPATCHER.message(Command('wake_up'))
async def start_wake_up(message: Message):
    """Обработчик события /wake_up."""
    await create_sleep(message.from_user.id, is_sleeping=False)
    response = await get_last_sleep(message.from_user.id)
    sleeping_hours = response.get('sleeping_hours')
    sleep_status = response.get('sleep_status')
    await message.answer(f'Вы спали {sleeping_hours} часов. {sleep_status}.')


async def test(chat_id: int):
    '''
    Тестовая функция для отправки сообщений ботом.
    '''
    await BOT.send_message(chat_id, choice(NOTIFICATIONS))


async def test_2(user: TelegramUser):
    '''
    Тестовая функция для отправки индивидуальных сообщений ботом.
    '''
    data = await backend_get(PROFILE_URL, user.token)
    if not isinstance(data, dict):
        name = data.json()['name']
        message = f'Вам, {name}, пора позаниматься!'
        await BOT.send_message(user.tg_user_id, message)


async def main():
    scheduler = AsyncIOScheduler()
    async with async_sessionmaker(ENGINE, expire_on_commit=False)() as session:
        users = (await session.scalars(select(TelegramUser))).all()
    # ОТПРАВКА СООБЩЕНИЯ РАЗ В ЧАС
    scheduler.add_job(test, 'interval', hours=1, args=(117508330,))
    # ОТПРАВКА ВСЕМ ПОЛЬЗОВАТЕЛЯМ РАЗ В 2 ЧАСА РАЗНЫХ СООБЩЕНИЙ
    for user in users:
        scheduler.add_job(test_2, 'interval', hours=2, args=(user, ))
    scheduler.start()
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
