import asyncio

from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram_forms import FormsManager
from config import BOT, DISPATCHER


@DISPATCHER.message(Command('start'))
async def start_message(message: Message):
    await message.answer(
        'Приветствую!\n'
        'Здесь должно быть большое описание, но пока в процессе разработки :)')


@DISPATCHER.message(Command('register'))
async def command_register(message: Message, forms: FormsManager):
    await message.answer('Давайте зарегиструемся!')
    await forms.show('registration')


async def main():
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
