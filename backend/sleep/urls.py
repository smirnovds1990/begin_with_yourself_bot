from django.urls import path

from sleep.views import SleepView, WakeUpView, get_last_sleep

urlpatterns = [
    path('<str:username>/sleep/', SleepView.as_view(), name='sleep'),
    path('<str:username>/wake_up/', WakeUpView.as_view(), name='wake_up'),
    path('<str:username>/last_sleep/', get_last_sleep, name='wake_up'),
]
