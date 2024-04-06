from django.urls import path

from sleep.views import get_last_sleep

urlpatterns = [
    path('last_sleep/', get_last_sleep, name='last_sleep'),
]
