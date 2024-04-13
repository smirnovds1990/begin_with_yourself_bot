from django.urls import path
from .views import (AvailableWorkoutTypesView,
                    UserWorkoutProgramView,
                    WorkoutDetailView,
                    WorkoutTypeList,
                    WorkoutTypeDetail)

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
    path(
        'user_workout_program_by_type/<int:workout_type_id>/',
        UserWorkoutProgramView.as_view(),
        name='user-workout-program-by-type'
    ),
    path(
        'available_workout_types/',
        AvailableWorkoutTypesView.as_view(),
        name='available-workout-types'
    ),
    path(
        'workouts/<int:pk>/',
        WorkoutDetailView.as_view(),
        name='workout-detail'
    ),
]
