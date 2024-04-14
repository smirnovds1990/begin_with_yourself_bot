# Generated by Django 4.2.11 on 2024-04-12 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('sex', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, verbose_name='Пол')),
                ('current_weight', models.FloatField(verbose_name='Текущий вес (кг.)')),
                ('sex', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, verbose_name='Пол')),
                ('current_weight', models.FloatField(verbose_name='Текущий вес (кг.)')),
                ('height', models.PositiveIntegerField(verbose_name='Рост (см.)')),
                ('birthdate', models.PositiveIntegerField(verbose_name='Год рождения')),
                ('aim', models.CharField(choices=[('gain', 'Набор'), ('loss', 'Сушка'), ('maintain', 'Поддержание')], max_length=10, null=True, verbose_name='Цель')),
                ('activity', models.CharField(choices=[('sedentary', 'Сидячий образ жизни'), ('light', 'Тренировки 1-3 раза в неделю'), ('moderate', 'Тренировки 3-5 раз в неделю'), ('intensive', 'Тренировки 6-7 раз в неделю'), ('athlete', 'Тренировки каждый день чаще чем раз в день')], max_length=20, null=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]
