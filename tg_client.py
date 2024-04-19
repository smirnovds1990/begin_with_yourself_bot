import asyncio
from hashlib import sha256
from random import choice

from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram_forms import FormsManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.sleep import (
    BAD_SLEEP_MESSAGE,
    GOOD_SLEEP_MESSAGE,
    GREAT_SLEEP_MESSAGE,
)
from telegram_client.config import BOT, DISPATCHER
from telegram_client.constants import NOTIFICATIONS
from telegram_client.db import ENGINE, TelegramUser
from telegram_client.functions import (
    create_sleep,
    create_token,
    get_last_sleep,
    get_profile,
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
                'но пока в процессе разработки :)\n'
                'Зарегистроваться: /register'
            )
        else:
            await message.answer('Вы уже прошли начальную регистрацию :)')


@DISPATCHER.message(Command('register'))
async def command_register(message: Message, forms: FormsManager):
    await message.answer('Давайте зарегиструемся!')
    await forms.show('registration')


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
    if sleep_status not in (
        BAD_SLEEP_MESSAGE,
        GOOD_SLEEP_MESSAGE,
        GREAT_SLEEP_MESSAGE,
    ):
        await message.answer(sleep_status)
    else:
        await message.answer(
            f'Вы спали {sleeping_hours} часов. Это {sleep_status}.'
        )


async def test(chat_id: int):
    '''
    Тестовая функция для отправки сообщений ботом.
    '''
    await BOT.send_message(chat_id, choice(NOTIFICATIONS))


async def test_2(user: TelegramUser):
    '''
    Тестовая функция для отправки индивидуальных сообщений ботом.
    '''
    # ЗАГЛУШКА. PROFILE НЕТ. БЕРЕМ USERNAME ИЗ AUTH
    name = (await get_profile(user.token))['username']
    #
    message = f'Вам, {name}, пора позаниматься!'
    await BOT.send_message(user.tg_user_id, message)


async def main():
    # ТЕСТИРОВАНИЕ ШЕДУЛЕРА
    scheduler = AsyncIOScheduler()
    async with async_sessionmaker(ENGINE, expire_on_commit=False)() as session:
        users = (await session.scalars(select(TelegramUser))).all()
    # ОТПРАВКА СООБЩЕНИЯ РАЗ В ЧАС
    scheduler.add_job(test, 'interval', hours=1, args=(117508330,))
    # ОТПРАВКА ВСЕМ ПОЛЬЗОВАТЕЛЯМ РАЗ В 2 ЧАСА РАЗНЫХ СООБЩЕНИЙ
    for user in users:
        scheduler.add_job(
            test_2,
            'interval',
            hours=2,
            args=(user, )
        )
    scheduler.start()
    #
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
