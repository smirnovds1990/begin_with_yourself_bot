from django.urls import path

from .views import calorie_norm

urlpatterns = [
    path('calorie-norm/', calorie_norm, name='calorie-norm'),
]
