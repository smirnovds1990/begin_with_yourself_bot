from django.db import models
from django.contrib.auth.models import User

from .constants import (GENDER_CHOICES,
                        ACTIVITY_CHOICES,
                        GOAL_CHOICES)



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
        max_length=15,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )
    aim = models.CharField(
        max_length=25,
        choices=GOAL_CHOICES,
        verbose_name='Цель',
        null=True
    )
    current_weight = models.PositiveIntegerField(
        verbose_name='Текущий вес (кг.)'
    )
    height = models.PositiveIntegerField(
        verbose_name='Рост (см.)'
    )
    birthdate = models.PositiveIntegerField(
        verbose_name='Год рождения'
    )
    activity = models.CharField(
        max_length=100,
        choices=ACTIVITY_CHOICES,
        verbose_name='Активность',
        null=True
    )

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
