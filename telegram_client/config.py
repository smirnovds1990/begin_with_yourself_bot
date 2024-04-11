from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, User
from aiogram_forms import Form, FormsManager
from aiogram_forms import dispatcher as dpf
from aiogram_forms import fields
from backend.profile.constants import (ACTIVITY_CHOICES, AIM_CHOICES,
                                       SEX_CHOICES)
from dotenv import load_dotenv

from .constants import (MAX_HEIGHT_LENGTH, MAX_NAME_LENGTH, MAX_WEIGHT_LENGTH,
                        MIN_LENGTH, YEAR_LENGTH)
from .functions import compile_registration_data, get_token, reverse_choices
from .validators import (validate_height, validate_name, validate_weight,
                         validate_year)

load_dotenv()

TOKEN = getenv('TOKEN')
BOT = Bot(TOKEN)
DISPATCHER = Dispatcher()


@dpf.register('training')
class TrainingForm(Form):
    aim = fields.ChoiceField(
        'Ваша цель', choices=reverse_choices(AIM_CHOICES))
    activity = fields.ChoiceField(
        'Наиболее подходящее описание вашего образа жизни',
        choices=reverse_choices(ACTIVITY_CHOICES)
    )
    current_weight = fields.TextField(
        'Ваш текущий вес',
        min_length=MIN_LENGTH,
        max_length=MAX_WEIGHT_LENGTH,
        validators=[validate_weight]
    )

    @classmethod
    async def callback(
            cls, message: Message,
            forms: FormsManager,
            **data):  # pylint: disable=arguments-differ
        user: User = data['event_from_user']
        form_data = await forms.get_data(TrainingForm)
        form_data['tg_user_id'] = user.id
        print(await get_token(message.from_user.id))
        print(form_data)
        #
        await message.answer('Отлично! Я зафиксировал данные :)')


@dpf.register('registration')
class RegisterForm(Form):
    name = fields.TextField(
        'Ваше имя',
        min_length=MIN_LENGTH,
        max_length=MAX_NAME_LENGTH,
        validators=[validate_name],
    )
    surname = fields.TextField(
        'Ваша фамилия',
        min_length=MIN_LENGTH,
        max_length=MAX_NAME_LENGTH,
        validators=[validate_name]
    )
    sex = fields.ChoiceField(
        'Выберите пол',
        choices=reversed(SEX_CHOICES)
    )
    height = fields.TextField(
        'Рост, в см',
        min_length=MIN_LENGTH,
        max_length=MAX_HEIGHT_LENGTH,
        validators=[validate_height]
    )
    birthdate = fields.TextField(
        'Год рождения',
        min_length=YEAR_LENGTH,
        max_length=YEAR_LENGTH,
        validators=[validate_year]
    )

    @classmethod
    async def callback(
            cls, message: Message,
            forms: FormsManager,
            **data):  # pylint: disable=arguments-differ
        '''
        Функция, возвращающая ответ на заполненную форму.
        '''
        user: User = data['event_from_user']
        form_data = await forms.get_data(RegisterForm)
        form_data['tg_user_id'] = user.id
        # ЗДЕСЬ ОТПРАВКА ПОСТ ЗАПРОСОВ В API Django
        print(await get_token(message.from_user.id))
        print(await compile_registration_data(form_data))
        #
        await message.answer(
            f'Поздравляю, {form_data["name"]}. Вы зарегистрированы!')
        await forms.show('training')


dpf.attach(DISPATCHER)
