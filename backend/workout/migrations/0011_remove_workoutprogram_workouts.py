# Generated by Django 4.2.11 on 2024-04-07 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0010_alter_workoutprogramdetail_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutprogram',
            name='workouts',
        ),
    ]
