from django.urls import path

from .views import CalorieNormView

urlpatterns = [
    path('calorie-norm/', CalorieNormView.as_view(), name='calorie-norm'),
]
