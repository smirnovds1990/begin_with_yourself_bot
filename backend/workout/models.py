from profile.constants import (SEX_CHOICES,
                               AIM_CHOICES)

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from .validators import validate_video_extension


class WorkoutType(models.Model):
    """
    Определяет тип тренировки,
    включая название и описание.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    icon = models.ImageField(
        upload_to='workout_icons/',
        blank=True,
        null=True,
        verbose_name='Иконка'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'тип тренировки'
        verbose_name_plural = 'типы тренировок'
        ordering = ['title']


class Workout(models.Model):
    """
    Определяет конкретную тренировку,
    включая её название, тип, описание и видео.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    workout_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.CASCADE,
        related_name='workouts',
        verbose_name='Тип тренировки'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    video = models.FileField(
        upload_to='workout_videos/',
        blank=True, null=True,
        validators=[validate_video_extension],
        verbose_name='Видео'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'тренировка'
        verbose_name_plural = 'тренировки'


class WorkoutProgram(models.Model):
    """
    Определяет программу тренировок, включая список тренировок,
    ориентированных на определенный пол и цель.
    Каждая программа уникальна по комбинации пола и цели.
    """
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол'
    )
    aim = models.CharField(
        max_length=10,
        choices=AIM_CHOICES,
        verbose_name='Цель'
    )

    def __str__(self):
        return (f'Программа тренировок - Пол: {self.get_sex_display()}, '
                f'Цель: {self.get_aim_display()}')

    class Meta:
        verbose_name = 'программа тренировок'
        verbose_name_plural = 'программы тренировок'
        unique_together = ('sex', 'aim')


class WorkoutProgramDetail(models.Model):
    workout_program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        related_name='program_details',
        verbose_name='Программа тренировок'
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        verbose_name='Тренировка'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        validators=[MinValueValidator(1)],
        blank=False,
        null=False
    )
    repetitions = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество повторений',
        blank=True,
        null=True
    )
    sets = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество подходов',
        blank=True,
        null=True
    )
    duration = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='Продолжительность (мин.)',
    )

    def __str__(self):
        description_parts = [f'{self.order}. {self.workout.title}']
        if self.repetitions:
            description_parts.append(
                f'Повторения: {self.repetitions}'
            )
        if self.sets:
            description_parts.append(
                f'Подходы: {self.sets}'
            )
        if self.duration:
            description_parts.append(
                f'Продолжительность: {self.duration}'
            )

        return ', '.join(description_parts)

    class Meta:
        verbose_name = 'элемент программы тренировок'
        verbose_name_plural = 'элементы программы тренировок'
        unique_together = ('workout_program', 'workout', 'order')
        ordering = ['order']


class UserWorkoutSession(models.Model):
    """
    Определяет пользовательскую сессию использования приложения тренировки.
    Сделана в разрезе типов тренировок,
    чтобы пользователь мог зайти в другой вид тренировок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    workout_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Тип тренировки'
    )
    current_workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Текущая тренировка'
    )
    completed_workouts = models.ManyToManyField(
        Workout,
        related_name='completed_workouts',
        verbose_name='Выполненные тренировки',
        blank=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время начала'
    )

    def __str__(self):
        session_info = f'Сессия {self.user.username}'
        if self.workout_type:
            session_info += f' - {self.workout_type.title}'
        return session_info

    class Meta:
        verbose_name = 'сессия тренировки пользователя'
        verbose_name_plural = 'сессии тренировки пользователей'
        ordering = ['-timestamp']
        unique_together = ('user', 'workout_type')
