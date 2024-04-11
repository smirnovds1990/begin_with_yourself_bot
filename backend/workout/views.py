from profile.models import UserProfile

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WorkoutType, WorkoutProgram
from .serializers import WorkoutTypeSerializer, WorkoutProgramSerializer
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

    def get(self, pk):
        workout_type = get_object_or_404(WorkoutType, id=pk)
        serializer = WorkoutTypeSerializer(workout_type)
        return Response(serializer.data)


class UserWorkoutProgramView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(
            UserProfile,
            user=request.user
        )
        workout_program = get_object_or_404(
            WorkoutProgram,
            sex=user_profile.sex,
            aim=user_profile.aim
        )
        serializer = WorkoutProgramSerializer(
            workout_program
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
