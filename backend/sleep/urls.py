from django.urls import include, path

from sleep.views import get_last_sleep, SleepViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', SleepViewSet, basename='sleep')

urlpatterns = [
    path('', include(router.urls)),
    path('last_sleep/', get_last_sleep, name='last_sleep'),
]
