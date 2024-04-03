from django.urls import path

from sleep.views import SleepView, WakeUpView, get_last_sleep

urlpatterns = [
    path('sleep/', SleepView.as_view(), name='sleep'),
    path('wake_up/', WakeUpView.as_view(), name='wake_up'),
    path('last_sleep/', get_last_sleep, name='last_sleep'),
]
