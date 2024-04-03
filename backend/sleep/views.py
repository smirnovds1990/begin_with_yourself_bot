from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from sleep.models import Sleep
from sleep.serializers import SleepSerializer

User = get_user_model()


class SleepView(APIView):
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        sleep = Sleep.objects.create(client=user)
        return Response(
            {'user': user.id, 'sleep_time': sleep.sleep_time},
            status=status.HTTP_201_CREATED,
        )


class WakeUpView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        latest_object = Sleep.objects.filter(client=user).first()
        if latest_object.wake_time:
            latest_object = Sleep.objects.create(
                wake_time=datetime.now(), is_sleeping=False, client=user
            )
        else:
            latest_object.wake_time = datetime.now()
            latest_object.is_sleeping = False
            latest_object.save()
        serializer = SleepSerializer(latest_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_last_sleep(request, username):
    user = get_object_or_404(User, username=username)
    latest_object = Sleep.objects.filter(client=user).first()
    serializer = SleepSerializer(latest_object)
    return Response(serializer.data, status=status.HTTP_200_OK)
