import asyncio
from datetime import datetime
from hashlib import sha256
from http import HTTPStatus
from random import choice
from urllib.parse import urljoin

from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from aiogram_forms import FormsManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from telegram_client.config import BOT, DISPATCHER, get_keyboard
from telegram_client.constants import (BASE_URL, NOTIFICATIONS, PROFILE_URL,
                                       WORKOUT_SESSION_URL, WORKOUT_URL,
                                       WORKOUT_USER_URL)
from telegram_client.db import ENGINE, TelegramUser
from telegram_client.functions import (backend_delete, backend_get,
                                       backend_post, create_token, get_token)


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
                'но пока в процессе разработки 😏\n'
                'Зарегистроваться: /register'
            )
        else:
            await message.answer(
                'Вы уже прошли начальную регистрацию 😏\n'
                'Продолжить: /register')


@DISPATCHER.callback_query(F.data == '/nutrition')
async def nutrilon_handler(callback: CallbackQuery):
    await callback.message.answer(
        'Callback `nutrition` function.')


@DISPATCHER.callback_query(F.data == '/sleep')
async def sleep_handler(callback: CallbackQuery):
    await callback.message.answer(
        'Callback `sleep` function.')


@DISPATCHER.callback_query(F.data == '/workout')
async def workout_handler(callback: CallbackQuery):
    user_token = await get_token(callback.from_user.id)
    program_details = await backend_get(WORKOUT_USER_URL, user_token)
    if HTTPStatus.NOT_FOUND == program_details.status:
        await callback.message.answer(
            'Увы, на вашы данные не найден коплекс упраждений 🥺')
    elif not isinstance(program_details, dict):
        program_details = await program_details.json()
        if 'program_details' in program_details.keys():
            buttons = []
            descriptions = []
            counter = 1
            for item in program_details['program_details']:
                workout = await backend_get(
                    urljoin(WORKOUT_URL, str(item['workout_id'])),
                    user_token)
                if not isinstance(workout, dict):
                    workout = await workout.json()
                    buttons.append(
                        [InlineKeyboardButton(
                            text=item['workout_title'],
                            callback_data=(
                                f'train_{workout["workout_type"]}-'
                                f'{item["workout_id"]}'))])
                    descriptions.append(
                        f'*{counter}. '
                        f'{item["workout_title"]}*\n'
                        f'{workout["description"]}\n')
                counter += 1

            descriptions = '\n'.join(descriptions)
            message = (
                'Исходя из вашего профиля, '
                'можем предложить следующие упражнения:\n'
                f'{descriptions}\n'
                'Начнем тренировку? 😏 '
                'Выбирайте упражнение и приступаем!')
            await callback.message.answer(
                message,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
                parse_mode='Markdown')
    else:
        await callback.message.answer(
            'Кажется, что-то пошло не так.\n'
            'Попробуйте еще раз или подойдите позже.')


@DISPATCHER.callback_query(F.data.startswith('train_'))
async def train_handler(callback: CallbackQuery):
    workout_data = callback.data.split('_')[-1].split('-')
    workout_type, workout_id = workout_data[0], workout_data[-1]
    user_token = await get_token(callback.from_user.id)
    workout = await backend_get(urljoin(WORKOUT_URL, workout_id), user_token)
    program_details = await backend_get(WORKOUT_USER_URL, user_token)
    if not isinstance(workout, dict) and not isinstance(program_details, dict):
        workout = await workout.json()
        program_details = (await program_details.json())['program_details']
        data = [
            item for item in program_details
            if item['workout_id'] == int(workout_id)
        ][0]
        buttons = [
            InlineKeyboardButton(
                text='Начать',
                callback_data=f'session_start_{workout_type}-{workout_id}'),
            InlineKeyboardButton(
                text='Закончить',
                callback_data=f'session_end_{workout_type}-{workout_id}'),
        ]
        message = (
            f'{workout["title"]}\n'
            f'{workout["description"]}\n\n'
            'Необходимо выполнить повторений за 1 подход: '
            f'{data["repetitions"]}\n'
            f'Всего подходов: {data["sets"]}\n'
            'Предполагаемая продолжительность занятия: '
            f'{data["duration"]} минут.\n'
        )
        if workout['video']:
            link = urljoin(BASE_URL, workout["video"])
            message = f'{message}\nВидео с упражнением:\n{link}'
        await callback.message.answer(
            message,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[buttons]),
            link_preview_options={'is_disabled': False})
    else:
        await callback.message.answer(
            'Кажется, что-то пошло не так.\n'
            'Попробуйте еще раз или подойдите позже.')


@DISPATCHER.callback_query(F.data.startswith('session_'))
async def workout_session_handler(callback: CallbackQuery):
    user_token = await get_token(callback.from_user.id)
    workouts = await backend_get(WORKOUT_SESSION_URL, user_token)
    if not isinstance(workouts, dict):
        workouts = await workouts.json()
        data = callback.data.split('_')
        session = data[1]
        workout_data = data[-1].split('-')
        workout_type, workout_id = workout_data[0], workout_data[1]
        if session == 'start' and not workouts:
            body = {
                'workout_type': workout_type,
                'current_workout': workout_id
            }
            start = await backend_post(
                WORKOUT_SESSION_URL,
                user_token,
                body)
            if not isinstance(start, dict):
                await callback.message.answer('🚀Поехали!🚀')
        elif session == 'end' and workouts:
            time = datetime.strptime(
                workouts[0]['timestamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            delete = await backend_delete(
                urljoin(WORKOUT_SESSION_URL, str(workouts[0]['id'])),
                user_token)
            if delete.status == HTTPStatus.NO_CONTENT:
                time = str(datetime.now() - time).split('.', maxsplit=1)[0]
                await callback.message.answer(
                    'Фух😮‍💨\nУпражнение закончили за '
                    f'{time}.\nПродолжим тренироваться или пойдем поедим? 😉',
                    reply_markup=get_keyboard()
                )
        elif workouts:
            await callback.message.answer(
                'Еще не закончено предыдущее занятие!😈')
        elif not workouts:
            await callback.message.answer('Мы еще даже не начинали!👀')
    else:
        await callback.message.answer(
            'Кажется, что-то пошло не так.\n'
            'Попробуйте еще раз или подойдите позже.')


@DISPATCHER.callback_query(F.data == '/renew')
async def renew_handler(callback: CallbackQuery):
    await callback.message.answer(
        'Для обновления ваших данных вызовите \n/renew 😏')


@DISPATCHER.message(Command('renew'))
async def command_renew(message: Message, forms: FormsManager):
    await message.answer('Давайте зафиксируем ваши данные.')
    await forms.show('training')


@DISPATCHER.message(Command('register'))
async def command_register(message: Message, forms: FormsManager):
    user_token = await get_token(message.from_user.id)
    status = await backend_get(PROFILE_URL, user_token)
    if not isinstance(status, dict):
        if status.status == HTTPStatus.OK:
            await message.answer(
                'Вы уже зарегистированы. '
                'Вероятно, кнопки ниже могут вам помочь 🤫',
                reply_markup=get_keyboard())
        elif status.status == HTTPStatus.NOT_FOUND:
            await message.answer('Давайте зарегиструемся!')
            await forms.show('registration')
        else:
            await message.answer(
                'Кажется, что-то пошло не так.\n'
                'Попробуйте еще раз или подойдите позже.')
    else:
        await message.answer(
            'Кажется, что-то пошло не так.\n'
            'Попробуйте еще раз или подойдите позже.')


async def test(chat_id: int):
    '''
    Тестовая функция для отправки сообщений ботом.
    '''
    await BOT.send_message(chat_id, choice(NOTIFICATIONS))


async def test_2(user: TelegramUser):
    '''
    Тестовая функция для отправки индивидуальных сообщений ботом.
    '''
    data = await backend_get(PROFILE_URL, user.token)
    if not isinstance(data, dict):
        name = (await data.json())['name']
        message = f'Вам, {name}, пора позаниматься!'
        await BOT.send_message(user.tg_user_id, message)


async def main():
    scheduler = AsyncIOScheduler()
    async with async_sessionmaker(ENGINE, expire_on_commit=False)() as session:
        users = (await session.scalars(select(TelegramUser))).all()
    # ОТПРАВКА СООБЩЕНИЯ РАЗ В ЧАС
    scheduler.add_job(test, 'interval', hours=1, args=(117508330,))
    # ОТПРАВКА ВСЕМ ПОЛЬЗОВАТЕЛЯМ РАЗ В 2 ЧАСА РАЗНЫХ СООБЩЕНИЙ
    for user in users:
        scheduler.add_job(test_2, 'interval', hours=2, args=(user, ))
    scheduler.start()
    await DISPATCHER.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
