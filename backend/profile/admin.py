from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'sex',
        'current_weight',
        'height',
        'birthdate',
        'aim',
        'activity'
    )
    search_fields = (
        'user__username',
        'user__email',
        'sex',
        'aim',
        'activity'
    )


admin.site.register(UserProfile, UserProfileAdmin)
