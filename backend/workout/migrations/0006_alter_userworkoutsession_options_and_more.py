# Generated by Django 4.2.11 on 2024-04-14 00:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workout', '0005_rename_usersession_userworkoutsession'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userworkoutsession',
            options={'ordering': ['-timestamp'], 'verbose_name': 'сессия тренировки пользователя', 'verbose_name_plural': 'сессии тренировки пользователей'},
        ),
        migrations.AlterField(
            model_name='userworkoutsession',
            name='workout_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workout.workouttype', verbose_name='Тип тренировки'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='userworkoutsession',
            unique_together={('user', 'workout_type')},
        ),
    ]
