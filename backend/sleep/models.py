from django.contrib.auth import get_user_model
from django.db import models

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
    def sleeping_hours(cls, user):
        last_sleep = Sleep.objects.filter(client=user).first()
        if not last_sleep:
            return 'Sleep not found'
        if last_sleep.is_sleeping:
            return 'User did not wake up'
        prelast_sleep = Sleep.objects.filter(client=user)[1]
        if not prelast_sleep.is_sleeping:
            return 'User did not start sleeping'
        return round(
            (last_sleep.sleep_time - prelast_sleep.sleep_time).seconds / 3600,
            2,
        )

    @classmethod
    def sleep_quality(cls, hours):
        if 0 <= hours < 6:
            return 'мало'
        if 6 <= hours <= 8:
            return 'хорошо'
        return 'отлично'

    class Meta:
        verbose_name = 'Сон'
        verbose_name_plural = 'Сны'
        ordering = ['-sleep_time']
