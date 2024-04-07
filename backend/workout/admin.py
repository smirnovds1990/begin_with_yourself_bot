from django.contrib import admin
from django.utils.html import format_html

from .models import (Workout,
                     WorkoutProgram,
                     WorkoutProgramDetail,
                     WorkoutType)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'workout_type',
        'video_preview'
    )
    search_fields = (
        'title',
        'workout_type__title'
    )
    list_filter = (
        'workout_type',
    )
    fields = (
        'title',
        'workout_type',
        'description',
        'video',
        'video_preview'
    )
    readonly_fields = (
        'video_preview',
    )

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="320" height="240" controls>'
                '<source src="{}" type="video/mp4">'
                'Ваш браузер не поддерживает видео тег.'
                '</video>', obj.video.url)
        return "Видео не загружено"
    video_preview.short_description = "Предпросмотр видео"


class WorkoutProgramDetailInline(admin.TabularInline):
    model = WorkoutProgramDetail
    extra = 1
    fields = (
        'workout',
        'order',
        'repetitions',
        'sets',
        'duration'
    )


class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = (
        'gender',
        'goal'
    )
    list_filter = (
        'gender',
        'goal'
    )
    search_fields = (
        'gender',
        'goal'
    )
    inlines = [WorkoutProgramDetailInline]


class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_active',
        'icon_preview'
    )
    fields = (
        'title',
        'description',
        'is_active',
        'icon',
        'icon_preview'
    )
    readonly_fields = (
        'icon_preview',
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.icon.url
            )
        return "Иконка не загружена"
    icon_preview.short_description = "Предварительный просмотр иконки"


admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutType, WorkoutTypeAdmin)
admin.site.register(WorkoutProgram, WorkoutProgramAdmin)
