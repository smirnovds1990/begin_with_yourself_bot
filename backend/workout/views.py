from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WorkoutType
from .serializers import WorkoutTypeSerializer
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
