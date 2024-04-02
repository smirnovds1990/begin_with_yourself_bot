from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram_forms import Form, FormsManager
from aiogram_forms import dispatcher as dpf
from aiogram_forms import fields
from constants import (DATE_LENGTH, MAX_HEIGHT_LENGTH, MAX_NAME_LENGTH,
                       MAX_WEIGHT_LENGTH, MIN_LENGTH)
from dotenv import load_dotenv
from functions import compile_registration_data
from validators import (validate_date, validate_height, validate_name,
                        validate_weight)

load_dotenv()

TOKEN = getenv('TOKEN')
BOT = Bot(TOKEN)
DISPATCHER = Dispatcher()


@dpf.register('registration')  # ФОРМЫ ТЕПЕРЬ ЗДЕСЬ
class RegisterForm(Form):
    first_name = fields.TextField(
        'Ваше имя',
        min_length=MIN_LENGTH,
        max_length=MAX_NAME_LENGTH,
        validators=[validate_name],
    )
    last_name = fields.TextField(
        'Ваша фамилия',
        min_length=MIN_LENGTH,
        max_length=MAX_NAME_LENGTH,
        validators=[validate_name]
    )
    sex = fields.ChoiceField(
        'Выберите пол',
        choices=(
            ('Мужской', 'М'),
            ('Женский', 'Ж')
        )
    )
    height = fields.TextField(
        'Рост, в см',
        min_length=MIN_LENGTH,
        max_length=MAX_WEIGHT_LENGTH,
        validators=[validate_height]
    )
    current_weight = fields.TextField(
        'Ваш текущий вес',
        min_length=MIN_LENGTH,
        max_length=MAX_HEIGHT_LENGTH,
        validators=[validate_weight]
    )
    birth_date = fields.TextField(
        'Дата рождения',
        min_length=DATE_LENGTH,
        max_length=DATE_LENGTH,
        validators=[validate_date]
    )

    @classmethod
    async def attach_to(cls, my_disp):
        '''
        Функция, привязывающая FormDispatcher в Диспатчеру бота.
        '''
        await dpf.attach(my_disp)

    @classmethod
    async def callback(cls, message: Message, forms: FormsManager, **data):
        '''
        Функция, возвращающая ответ на заполненную форму.
        '''
        data = await forms.get_data(RegisterForm)
        print(await compile_registration_data(data))  # Для тестирования
        await message.answer(f'Спасибо за регистрацию, {data["first_name"]}!')


dpf.attach(DISPATCHER)
