from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from sleep.models import Sleep
from sleep.serializers import SleepSerializer


class ListCreateViewSet(
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class SleepViewSet(ListCreateViewSet):
    queryset = Sleep.objects.all()
    serializer_class = SleepSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


@api_view(['GET'])
def get_last_sleep(request):
    sleep_result = Sleep.sleeping_hours(request.user)
    if isinstance(sleep_result, str):
        return Response({'Result': sleep_result}, status.HTTP_404_NOT_FOUND)
    return Response(
        {
            'sleeping_hours': sleep_result,
            'sleep_quality': Sleep.sleep_quality(sleep_result),
        },
        status=status.HTTP_200_OK,
    )
