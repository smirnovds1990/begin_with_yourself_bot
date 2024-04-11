from django.urls import path
from .views import (WorkoutTypeList,
                    WorkoutTypeDetail,
                    UserWorkoutProgramView)

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
    path(
        'user_workout_program/',
        UserWorkoutProgramView.as_view(),
        name='user-workout-program'
    ),
]
