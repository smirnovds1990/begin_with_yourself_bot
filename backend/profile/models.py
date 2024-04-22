from django.contrib.auth.models import User
from django.db import models

from .constants import ACTIVITY_CHOICES, AIM_CHOICES, SEX_CHOICES


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        primary_key=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Имя пользователя'
    )
    surname = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол'
    )
    current_weight = models.FloatField(
        verbose_name='Текущий вес (кг.)',
        null=True
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
        verbose_name='Цель',
        null=True
    )
    activity = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        verbose_name='Активность',
        null=True
    )

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
