from django.contrib import admin
from sleep.models import Sleep


@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    """Настройка модели Sleep в админке."""

    list_display = (
        'id',
        'sleep_time',
        'is_sleeping',
        'client',
    )
    list_filter = ('sleep_time', 'client')
    search_fields = (
        'sleep_time',
        'client',
    )
