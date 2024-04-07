from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions

from sleep.views import SleepViewSet

router = routers.DefaultRouter()
router.register('sleep', SleepViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='"Начни с себя" API',
        default_version='v1',
        description='Документация для проекта "Начни с себя"',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'nutrition/',
        include('nutrition.urls')
    ),
    path(
        'workout/',
        include('workout.urls')
    ),
    path(
        'swagger<format>/',
        schema_view.without_ui(
            cache_timeout=0
        ),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='schema-redoc'
    ),
    path('api/sleep/', include('sleep.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
