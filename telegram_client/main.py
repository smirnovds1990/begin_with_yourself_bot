import asyncio
from hashlib import sha256
from random import choice

from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram_forms import FormsManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import BOT, DISPATCHER, ENGINE
from constants import NOTIFICATIONS
from db import TgUser
from functions import get_token


@DISPATCHER.message(Command('start'))
async def start_message(message: Message):
    row = {
        'username': f'{message.from_user.id}',
        'password': sha256(f'{message.from_user.id}'.encode()).hexdigest()
    }
    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    query = select(TgUser).where(TgUser.tg_user_id == message.from_user.id)
    async with async_session() as session:
        user = (await session.scalars(query)).one_or_none()
        if not user:
            row['token'] = await get_token(row)
            row['tg_user_id'] = message.from_user.id
            session.add(TgUser(**row))
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


async def test(chat_id: int):
    '''
    Тестовая функция для отправки сообщений ботом.
    '''
    await BOT.send_message(chat_id, choice(NOTIFICATIONS))


async def main():
    # В РАМКАХ ТЕСТОВ ИСПОЛЬЗУЕТСЯ МОЙ CHAT_ID
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, 'interval', hours=1, args=(117508330,))
    scheduler.start()
    #
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
