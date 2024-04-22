from django_filters import rest_framework as filters

from .models import WorkoutType


class WorkoutTypeFilter(filters.FilterSet):
    class Meta:
        model = WorkoutType
        fields = ['is_active']
