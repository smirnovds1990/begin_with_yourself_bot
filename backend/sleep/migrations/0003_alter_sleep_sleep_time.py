# Generated by Django 4.2.11 on 2024-04-09 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sleep", "0002_remove_sleep_wake_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sleep",
            name="sleep_time",
            field=models.DateTimeField(verbose_name="Время сна"),
        ),
    ]
