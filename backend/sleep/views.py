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
    last_sleep = Sleep.objects.filter(client=request.user).first()
    if not last_sleep:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SleepSerializer(last_sleep)
    return Response(serializer.data, status=status.HTTP_200_OK)
