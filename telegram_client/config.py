from os import getenv

from aiogram import Bot, Dispatcher
from aiogram_forms import dispatcher as dpf
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')
BOT = Bot(TOKEN)
DISPATCHER = Dispatcher()

dpf.attach(DISPATCHER)
