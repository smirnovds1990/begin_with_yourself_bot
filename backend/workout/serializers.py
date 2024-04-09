from rest_framework import serializers
from .models import WorkoutType


class WorkoutTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = [
            'id',
            'title',
            'description',
            'is_active',
            'icon'
        ]
