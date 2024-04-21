from django.urls import include, path
from rest_framework import routers

from sleep.views import SleepViewSet, get_last_sleep

router = routers.DefaultRouter()
router.register('', SleepViewSet, basename='sleep')

urlpatterns = [
    path('', include(router.urls)),
    path('last_sleep/', get_last_sleep, name='last_sleep'),
]
