from profile.models import UserProfile

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Workout,
                     WorkoutType,
                     WorkoutProgram,
                     WorkoutProgramDetail)
from .serializers import (WorkoutSerializer,
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
