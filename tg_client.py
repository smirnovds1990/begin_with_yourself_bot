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
from telegram_client.functions import backend_get, create_token, get_token


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


@DISPATCHER.callback_query(F.data == '/training')
async def training_handler(callback: CallbackQuery):
    await callback.message.answer('/training handler message.')


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
    if (await backend_get(
         PROFILE_URL, user_token
         )).status_code == HTTPStatus.NOT_FOUND:
        await message.answer('Давайте зарегиструемся!')
        await forms.show('registration')
    else:
        await message.answer(
            'Вы уже зарегистированы. Вероятно, кнопки ниже могут вам помочь 🤫',
            reply_markup=get_keyboard())


async def test(chat_id: int):
    '''
    Тестовая функция для отправки сообщений ботом.
    '''
    await BOT.send_message(chat_id, choice(NOTIFICATIONS))


async def test_2(user: TelegramUser):
    '''
    Тестовая функция для отправки индивидуальных сообщений ботом.
    '''
    name = (await backend_get(PROFILE_URL, user.token))['name']
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
