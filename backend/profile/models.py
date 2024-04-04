from django.db import models
from django.contrib.auth.models import User

from .constants import (GENDER_CHOICES,
                        ACTIVITY_CHOICES,
                        GOAL_CHOICES)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )
    current_weight = models.PositiveIntegerField(
        verbose_name='Текущий вес (кг.)'
    )
    height = models.PositiveIntegerField(
        verbose_name='Рост (см.)'
    )
    year_of_birth = models.PositiveIntegerField(
        verbose_name='Год рождения'
    )
    goal = models.CharField(
        max_length=10,
        choices=GOAL_CHOICES,
        verbose_name='Цель'
    )
    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        verbose_name='Активность'
    )
