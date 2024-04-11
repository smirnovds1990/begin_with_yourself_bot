from django.db import models
from django.contrib.auth.models import User

from .constants import (SEX_CHOICES,
                        ACTIVITY_CHOICES,
                        AIM_CHOICES)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол'
    )
    current_weight = models.FloatField(
        verbose_name='Текущий вес (кг.)'
    )
    height = models.PositiveIntegerField(
        verbose_name='Рост (см.)'
    )
    birthdate = models.PositiveIntegerField(
        verbose_name='Год рождения'
    )
    aim = models.CharField(
        max_length=10,
        choices=AIM_CHOICES,
        verbose_name='Цель'
    )
    activity = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        verbose_name='Активность'
    )

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
