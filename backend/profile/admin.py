from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'surname',
        'sex',
        'current_weight',
        'height',
        'birthdate',
        'aim',
        'activity'
    )
    search_fields = (
        'user__username',
        'sex',
        'aim',
        'activity'
    )


admin.site.register(UserProfile, UserProfileAdmin)
