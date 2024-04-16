from profile.models import UserProfile

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (UserWorkoutSession,
                     Workout,
                     WorkoutType,
                     WorkoutProgram,
                     WorkoutProgramDetail)
from .serializers import (UserWorkoutSessionSerializer,
                          WorkoutSerializer,
                          WorkoutTypeSerializer,
                          WorkoutProgramSerializer)
from .filters import WorkoutTypeFilter


class WorkoutTypeList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'is_active',
            openapi.IN_QUERY,
            description="Активен",
            type=openapi.TYPE_BOOLEAN
        )
    ])
    def get(self, request):
        '''
        Получение списка типов тренировок с фильтрацией
        '''
        workout_types = WorkoutTypeFilter(
            request.GET,
            queryset=WorkoutType.objects.all()
        )
        serializer = WorkoutTypeSerializer(
            workout_types.qs,
            many=True
        )
        return Response(
            serializer.data
        )

    @swagger_auto_schema(request_body=WorkoutTypeSerializer)
    def post(self, request):
        '''
        Создание типа тренировок
        '''
        serializer = WorkoutTypeSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


class WorkoutTypeDetail(APIView):
    '''
    Получение типа тренировок по id
    '''

    def get(self, pk):
        workout_type = get_object_or_404(WorkoutType, id=pk)
        serializer = WorkoutTypeSerializer(workout_type)
        return Response(serializer.data)


class BaseUserWorkoutProgramView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_workout_program(self, request):
        '''
        Получает программу тренировок доступную текущему пользователю
        '''
        user_profile = get_object_or_404(
            UserProfile, user=request.user
        )
        return get_object_or_404(
            WorkoutProgram,
            sex=user_profile.sex,
            aim=user_profile.aim
        )


class UserWorkoutProgramView(BaseUserWorkoutProgramView):
    def get(self, request, **kwargs):
        '''
        Получение текущей программы тренировок с упражнениями.
        В сериализаторе указан отбор только упражнений
        с активным типом тренировок. Возможен отбор по
        id типа тренировок.
        '''
        workout_program = self.get_user_workout_program(
            request
        )
        context = {
            'filter_active': True,
        }

        workout_type_id = kwargs.get('workout_type_id')
        if workout_type_id:
            context['workout_type_id'] = workout_type_id

        serializer = WorkoutProgramSerializer(
            workout_program,
            context=context
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AvailableWorkoutTypesView(BaseUserWorkoutProgramView):
    def get(self, request):
        '''
        Получение списка активных типов тренировок
        по программе тренировок текущего пользователя
        '''
        workout_program = self.get_user_workout_program(
            request
        )
        workout_ids = WorkoutProgramDetail.objects.filter(
            workout_program=workout_program
        ).values_list(
            'workout__workout_type',
            flat=True
        ).distinct()
        workout_types = WorkoutType.objects.filter(
            id__in=workout_ids,
            is_active=True
        )
        serializer = WorkoutTypeSerializer(
            workout_types,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WorkoutDetailView(APIView):
    def get(self, pk):
        '''
        Получение данных конкретной тренировки
        '''
        workout = get_object_or_404(
            Workout,
            id=pk
        )
        serializer = WorkoutSerializer(
            workout
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WorkoutSessionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserWorkoutSessionSerializer,
        responses={201: UserWorkoutSessionSerializer}
    )
    def post(self, request):
        serializer = UserWorkoutSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        sessions = UserWorkoutSession.objects.filter(
            user=request.user
        )
        serializer = UserWorkoutSessionSerializer(
            sessions,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WorkoutSessionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(
            UserWorkoutSession,
            pk=session_id,
            user=request.user
        )
        serializer = UserWorkoutSessionSerializer(
            session
        )
        return Response(
            serializer.data
        )

    @swagger_auto_schema(
        request_body=UserWorkoutSessionSerializer,
        responses={200: UserWorkoutSessionSerializer()}
    )
    def patch(self, request, session_id):

        session = get_object_or_404(
            UserWorkoutSession,
            pk=session_id,
            user=request.user
        )

        if 'current_workout' in request.data:
            current_workout_id = request.data.get('current_workout')
            if current_workout_id:
                current_workout = get_object_or_404(
                    Workout,
                    pk=current_workout_id
                )
                session.current_workout = current_workout
            else:
                session.current_workout = None

        completed_workout_id = request.data.get('complete_workout')
        if completed_workout_id:
            completed_workout = get_object_or_404(
                Workout,
                pk=completed_workout_id
            )
            session.completed_workouts.add(completed_workout)

        session.save()
        serializer = UserWorkoutSessionSerializer(
            session
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, session_id):
        session = get_object_or_404(
            UserWorkoutSession,
            pk=session_id,
            user=request.user
        )
        session.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class SessionAvailableWorkoutView(BaseUserWorkoutProgramView):
    def get(self, request, session_id):

        session = get_object_or_404(
            UserWorkoutSession,
            pk=session_id
        )

        workout_program = self.get_user_workout_program(
            request
        )

        completed_workouts_ids = session.completed_workouts.values_list(
            'id',
            flat=True
        )

        workout_details = workout_program.program_details.exclude(
            workout__id__in=completed_workouts_ids
        ).filter(
            workout__workout_type_id=session.workout_type
        ).order_by(
            'order'
        ).first()

        if workout_details:
            serializer = WorkoutSerializer(workout_details.workout)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Нет доступных тренировок"},
            status=status.HTTP_200_OK
        )
