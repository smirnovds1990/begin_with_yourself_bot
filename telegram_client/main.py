import asyncio

from aiogram.filters.command import Command
from aiogram.types import Message

from config import BOT, DISPATCHER


@DISPATCHER.message(Command('start'))
async def start_message(message: Message):
    await message.answer(
        'Приветствую!\n'
        'Здесь должно быть большое описание, но пока в процессе разработки :)')


async def main():
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
