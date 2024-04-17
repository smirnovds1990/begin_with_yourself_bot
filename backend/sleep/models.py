from django.contrib.auth import get_user_model
from django.db import models

from sleep.constants import (
    GOOD_SLEEP_FRONTIER,
    GREAT_SLEEP_FRONTIER,
    MAX_SLEEPING_HOURS_FRONTIER,
)

BAD_SLEEP_MESSAGE = 'мало'
GOOD_SLEEP_MESSAGE = 'хорошо'
GREAT_SLEEP_MESSAGE = 'отлично'
SLEEP_NOT_FOUND_MESSAGE = 'Sleep not found'
NOT_WAKE_UP_MESSAGE = 'User did not wake up'
NOT_START_SLEEPING_MESSAGE = 'User did not start sleeping'

User = get_user_model()


class Sleep(models.Model):
    """Модель сна пользователя."""

    sleep_time = models.DateTimeField(
        verbose_name='Время сна', auto_now_add=True
    )
    is_sleeping = models.BooleanField(
        verbose_name='Признак "лёг"', default=True
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sleep',
        verbose_name='Пользователь',
    )

    @classmethod
    def sleeping_status(cls, user):
        """Возвращает статус последнего сна."""
        last_sleep = (
            Sleep.objects.filter(client=user).order_by('-sleep_time').first()
        )
        if not last_sleep:
            return (0, SLEEP_NOT_FOUND_MESSAGE)
        if last_sleep.is_sleeping:
            return (0, NOT_WAKE_UP_MESSAGE)
        prelast_sleep = Sleep.objects.filter(client=user).order_by(
            '-sleep_time'
        )[1]
        if not prelast_sleep.is_sleeping:
            return (0, NOT_START_SLEEPING_MESSAGE)
        hours = round(
            (last_sleep.sleep_time - prelast_sleep.sleep_time).seconds / 3600,
            2,
        )
        return (
            (hours, cls.sleep_quality(hours))
            if hours < MAX_SLEEPING_HOURS_FRONTIER
            else (0, NOT_WAKE_UP_MESSAGE)
        )

    @classmethod
    def sleep_quality(cls, hours):
        """Возвращает качества сна."""
        if hours < GOOD_SLEEP_FRONTIER:
            return BAD_SLEEP_MESSAGE
        if GOOD_SLEEP_FRONTIER <= hours <= GREAT_SLEEP_FRONTIER:
            return GOOD_SLEEP_MESSAGE
        return GREAT_SLEEP_MESSAGE

    class Meta:
        verbose_name = 'Сон'
        verbose_name_plural = 'Сны'
        ordering = ['-sleep_time']
