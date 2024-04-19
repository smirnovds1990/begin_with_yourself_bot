from django.urls import path

from .views import CalorieNormView

urlpatterns = [
    path('', CalorieNormView.as_view(), name='calorie-norm'),
]
