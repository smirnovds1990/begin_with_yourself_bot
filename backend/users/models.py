from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


SEX_CHOICES = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)

ACTIVITY_CHOICES = (
    ('sedentary', 'Сидячий образ жизни'),
    ('light', 'Тренировки 1-3 раза в неделю'),
    ('moderate', 'Тренировки 3-5 раз в неделю'),
    ('intensive', 'Тренировки 6-7 раз в неделю'),
    ('athlete', 'Тренировки каждый день чаще чем раз в день'),
)

AIM_CHOICE = (
    ('gain', 'Набор'),
    ('loss', 'Сушка'),
    ('maintain', 'Поддержание'),
)


class CustomUser(AbstractUser):
    """Модель Пользователя."""
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        },
        validators=[
            validators.RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Недопустимое значение!',
            ),
        ],
    )
    surname = models.CharField('Фамилия', max_length=150)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол',
        default='M'
    )
    aim = models.CharField(max_length=25, choices=AIM_CHOICE)
    current_weight = models.PositiveIntegerField(
        verbose_name='Текущий вес (кг.)'
    )
    height = models.PositiveIntegerField(verbose_name='Рост (см.)')
    birthdate = models.PositiveIntegerField(verbose_name='Год рождения')
    activity = models.CharField(
        max_length=25,
        choices=ACTIVITY_CHOICES,
        verbose_name='Активность'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'sex',
        'current_weight',
        'height',
        'birthdate',
        'activity',
    ]

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_auth',
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
