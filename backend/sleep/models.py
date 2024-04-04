from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Sleep(models.Model):
    """Модель сна пользователя."""

    sleep_time = models.DateTimeField(
        verbose_name='Время сна', auto_now_add=True
    )
    wake_time = models.DateTimeField(
        verbose_name='Время пробуждения',
        null=True,
        blank=True,
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

    class Meta:
        verbose_name = 'Сон'
        verbose_name_plural = 'Сны'
        ordering = ['-sleep_time']
