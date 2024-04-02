from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username',
        'sex',
        'current_weight',
        'height',
        'birthdate',
        'activity',
    ]


admin.site.register(CustomUser, CustomUserAdmin)
