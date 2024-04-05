from django.db import models

from profile.constants import (GENDER_CHOICES,
                               GOAL_CHOICES)

from .validators import validate_video_extension


class WorkoutType(models.Model):
    """
    Определяет тип тренировки, включая название и описание.
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
        return self.title

    class Meta:
        verbose_name = 'тип тренировки'
        verbose_name_plural = 'типы тренировок'


class Workout(models.Model):
    """
    Определяет конкретную тренировку, включая её название, тип, описание и видео.
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
        return self.title

    class Meta:
        verbose_name = 'тренировка'
        verbose_name_plural = 'тренировки'


class WorkoutProgram(models.Model):
    """
    Определяет программу тренировок, включая список тренировок,
    ориентированных на определенный пол и цель.
    Каждая программа уникальна по комбинации пола и цели.
    """
    workouts = models.ManyToManyField(
        Workout,
        related_name='programs',
        verbose_name='тренировки'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )
    goal = models.CharField(
        max_length=10,
        choices=GOAL_CHOICES,
        verbose_name='Цель'
    )

    def __str__(self):
        return f"{self.get_gender_display()} - {self.get_goal_display()}"

    class Meta:
        verbose_name = 'программа тренировок'
        verbose_name_plural = 'программы тренировок'
        unique_together = ('gender', 'goal')
