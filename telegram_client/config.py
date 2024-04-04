from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, User
from aiogram_forms import Form, FormsManager
from aiogram_forms import dispatcher as dpf
from aiogram_forms import fields
from dotenv import load_dotenv

from constants import (DATE_LENGTH, MAX_HEIGHT_LENGTH, MAX_NAME_LENGTH,
                       MAX_WEIGHT_LENGTH, MIN_LENGTH)
from functions import compile_registration_data
from validators import (validate_date, validate_height, validate_name,
                        validate_weight)

load_dotenv()

TOKEN = getenv('TOKEN')
BOT = Bot(TOKEN)
DISPATCHER = Dispatcher()


@dpf.register('training')
class TrainingForm(Form):
    aim = fields.ChoiceField(
        'Ваша цель',
        choices=(
            ('Набор массы', 'MASS'),
            ('Поддержание', 'KEEP'),
            ('Похудание', 'LOSS')
        )
    )
    activity = fields.ChoiceField(
        'Наиболее подходящее описание вашего образа жизни',
        choices=(
            ('Сидячий образ жизни', 'PASS'),
            ('Тренировки от 30 мин 1-3 раза в неделю', 'TR13'),
            ('Тренировки 3-5 раза в неделю', 'TR35'),
            ('Интенсивные тренировки 6-7 раз в неделю', 'TR67'),
            ('Тренировки каждый день', 'TRED')
        )
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
        # ЗДЕСЬ PATCH ЗАПРОС В API Django
        print(form_data)
        #
        await message.answer('Отлично! Я зафиксировал данные :)')


@dpf.register('registration')
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
        max_length=MAX_HEIGHT_LENGTH,
        validators=[validate_height]
    )
    birth_date = fields.TextField(
        'Дата рождения',
        min_length=DATE_LENGTH,
        max_length=DATE_LENGTH,
        validators=[validate_date]
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
        print(await compile_registration_data(form_data))
        #
        await message.answer(
            f'Поздравляю, {form_data["first_name"]}. Вы зарегистрированы!')
        await forms.show('training')


dpf.attach(DISPATCHER)
