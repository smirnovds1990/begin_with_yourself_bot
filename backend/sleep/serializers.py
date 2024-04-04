from rest_framework import serializers

from sleep.models import Sleep


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = (
            'id',
            'sleep_time',
            'wake_time',
            'is_sleeping',
            'client',
        )
