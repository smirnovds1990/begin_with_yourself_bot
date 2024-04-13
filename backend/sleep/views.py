from rest_framework import viewsets
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
    """Вьюсет создания сна."""

    queryset = Sleep.objects.all()
    serializer_class = SleepSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


@api_view(['GET'])
def get_last_sleep(request):
    """Получает результат последнего сна пользователя."""
    sleeping_hours, sleep_status = Sleep.sleeping_hours(request.user)
    return Response(
        {
            'sleeping_hours': sleeping_hours,
            'sleep_status': sleep_status,
        },
    )
