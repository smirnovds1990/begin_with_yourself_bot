import re

from aiogram_forms.errors import ValidationError

from .constants import (BIRTH_YEAR_PATTERN, HEIGHT_PATTERN, NAMES_PATTERN,
                        WIGHT_PATTERN)


async def validate_name(value: str):
    if not re.match(NAMES_PATTERN, value):
        raise ValidationError('Только русский алфавит.', 'ERR_VAL_NAME')


async def validate_height(value: str):
    if not re.match(HEIGHT_PATTERN, value):
        raise ValidationError(
            'Введите Ваш рост в сантиментрах.', 'ERR_VAL_HEIGHT')


async def validate_weight(value: str):
    if not re.match(WIGHT_PATTERN, value):
        raise ValidationError(
            'Введите Ваш вес в формате <kg>.<g>. Например, 70.0 или 70.',
            'ERR_VAL_WEIGHT')


async def validate_year(value: str):
    if not re.match(BIRTH_YEAR_PATTERN, value):
        raise ValidationError(
            'Введите ваш год рождения в формате YYYY.', 'ERR_VAL_BY')
