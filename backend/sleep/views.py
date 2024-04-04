from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from sleep.models import Sleep
from sleep.serializers import SleepSerializer


class SleepView(APIView):
    def post(self, request):
        sleep = Sleep.objects.create(client=request.user)
        return Response(
            {'user': sleep.client, 'sleep_time': sleep.sleep_time},
            status=status.HTTP_201_CREATED,
        )


class WakeUpView(APIView):
    def post(self, request):
        last_sleep = Sleep.objects.filter(client=request.user).first()
        if not last_sleep or last_sleep.wake_time:
            last_sleep = Sleep.objects.create(
                wake_time=datetime.now(),
                is_sleeping=False,
                client=request.user,
            )
        else:
            last_sleep.wake_time = datetime.now()
            last_sleep.is_sleeping = False
            last_sleep.save()
        serializer = SleepSerializer(last_sleep)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_last_sleep(request):
    last_sleep = Sleep.objects.filter(client=request.user).first()
    if not last_sleep:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SleepSerializer(last_sleep)
    return Response(serializer.data, status=status.HTTP_200_OK)
