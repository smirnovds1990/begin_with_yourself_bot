import asyncio
from random import choice

from aiogram.filters.command import Command
from aiogram.types import Message, User
from aiogram_forms import FormsManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import BOT, DISPATCHER
from .constants import NOTIFICATIONS


@DISPATCHER.message(Command('start'))
async def start_message(message: Message):
    user: User = message.from_user
    username = f'{user.id}'
    print(username)  # Юзернейм для регистрации в API
    await message.answer(
        'Приветствую!\n'
        'Здесь должно быть большое описание, '
        'но пока в процессе разработки :)\n'
        'Зарегистроваться: /register'
    )


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
