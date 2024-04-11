from django.urls import path
from .views import WorkoutTypeList, WorkoutTypeDetail

urlpatterns = [
    path(
        'workout_types/',
        WorkoutTypeList.as_view(),
        name='workout-type-list'
    ),
    path(
        'workout_types/<int:id>/',
        WorkoutTypeDetail.as_view(),
        name='workout-type-detail'
    ),
]
