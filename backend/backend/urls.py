from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions

from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='"Begin with yourself" API',
        default_version='v1',
        description='Documentation for the project "Begin with yourself"',
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
        'api/',
        include(router.urls)
    ),
    path(
        'nutrition/',
        include('nutrition.urls')
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
]
