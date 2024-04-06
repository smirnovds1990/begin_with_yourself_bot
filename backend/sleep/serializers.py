from rest_framework import serializers

from sleep.models import Sleep


class SleepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sleep
        fields = (
            'id',
            'sleep_time',
            'is_sleeping',
        )

    def create(self, validated_data):
        client = self.context.get('request').user
        return Sleep.objects.create(client=client, **validated_data)
