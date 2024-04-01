from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gender',
        'current_weight',
        'height',
        'year_of_birth',
        'goal',
        'activity_level'
    )
    search_fields = (
        'user__username',
        'user__email',
        'gender',
        'goal',
        'activity_level'
    )


admin.site.register(UserProfile, UserProfileAdmin)
