from django.urls import path

from .views import (AvailableWorkoutTypesView, SessionAvailableWorkoutView,
                    UserWorkoutProgramView, WorkoutDetailView,
                    WorkoutSessionDetailAPIView,
                    WorkoutSessionListCreateAPIView, WorkoutTypeDetail,
                    WorkoutTypeList)

urlpatterns = [
    path(
        'workout_types/',
        WorkoutTypeList.as_view(),
        name='workout-type-list'
    ),
    path(
        'workout_types/<int:pk>/',
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
        '<int:pk>/',
        WorkoutDetailView.as_view(),
        name='workout-detail'
    ),
    path(
        'workout-session/',
        WorkoutSessionListCreateAPIView.as_view(),
        name='workout-session-list-create'
    ),
    path('workout-session/<int:session_id>/',
         WorkoutSessionDetailAPIView.as_view(),
         name='workout-session-detail'),
    path(
        'workout-session/<int:session_id>/available-workout/',
        SessionAvailableWorkoutView.as_view(),
        name='available-workout'
    ),
]
