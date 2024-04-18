from http import HTTPStatus
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_forms import Form, FormsManager
from aiogram_forms import dispatcher as dpf
from aiogram_forms import fields
from dotenv import load_dotenv

from .constants import (ACTIVITY_CHOICES, AIM_CHOICES, MAX_HEIGHT_LENGTH,
                        MAX_NAME_LENGTH, MAX_WEIGHT_LENGTH, MIN_LENGTH,
                        PROFILE_URL, SEX_CHOICES, USER_URL, YEAR_LENGTH)
from .functions import (backend_get, backend_post, compile_registration_data,
                        get_token, patch_profile, reverse_choices)
from .validators import (validate_height, validate_name, validate_weight,
                         validate_year)

load_dotenv()

TOKEN = getenv('TOKEN')
BOT = Bot(TOKEN)
DISPATCHER = Dispatcher()


def get_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text='Питание',
            callback_data='/nutrition'),
        InlineKeyboardButton(
            text='Сон',
            callback_data='/sleep'),
        InlineKeyboardButton(
            text='Тренировка',
            callback_data='/training'),
        InlineKeyboardButton(
            text='Обновить',
            callback_data='/renew'),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@dpf.register('training')
class TrainingForm(Form):
    aim = fields.ChoiceField(
        'Ваша цель 🎯', choices=reverse_choices(AIM_CHOICES))
    activity = fields.ChoiceField(
        'Наиболее подходящее описание вашего образа жизни 🤸🏼‍♀️',
        choices=reverse_choices(ACTIVITY_CHOICES)
    )
    current_weight = fields.TextField(
        'Ваш текущий вес ⚖️',
        min_length=MIN_LENGTH,
        max_length=MAX_WEIGHT_LENGTH,
        validators=[validate_weight]
    )

    @classmethod
    async def callback(
            cls, message: Message,
            forms: FormsManager,
            **data):  # pylint: disable=arguments-differ
        form_data = await forms.get_data(TrainingForm)
        user_token = await get_token(message.from_user.id)
        user_data = form_data
        user_data['user'] = (
            await backend_get(USER_URL, user_token)).json()['id']
        await patch_profile(user_token, user_data)
        await message.answer(
            'Отлично! Я зафиксировал данные 😏',
            reply_markup=get_keyboard())


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
        choices=reverse_choices(SEX_CHOICES)
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
        form_data = await forms.get_data(RegisterForm)
        user_token = await get_token(message.from_user.id)
        user_data = await compile_registration_data(form_data)
        user_data['user'] = (
            await backend_get(USER_URL, user_token)).json()['id']
        status = (await backend_post(
            PROFILE_URL, user_token, user_data)).status_code
        if status == HTTPStatus.CREATED:
            await message.answer(
                f'Поздравляю, {form_data["name"]}!🥳\nВы зарегистрированы!')
            await forms.show('training')
        else:
            await message.answer('Мне кажется, вы уже зарегистрированы 🤔')


dpf.attach(DISPATCHER)
