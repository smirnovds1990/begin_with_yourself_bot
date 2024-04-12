from rest_framework.routers import DefaultRouter

from django.urls import include, path

from profile.views import UserProfileViewSet


router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
