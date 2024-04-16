from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'name',
            'surname',
            'sex',
            'current_weight',
            'height',
            'birthdate',
            'aim',
            'activity'
        ]
        optional = [
            'current_weight',
            'aim',
            'activity'
        ]

    def validate_current_weight(self, value):
        if not value > 0:
            raise serializers.ValidationError(
                'The current_weight must be greater than zero!'
            )
        return value

    def validate_height(self, value):
        if not value > 0:
            raise serializers.ValidationError(
                'The height must be greater than zero!'
            )
        return value

    def validate_birthdate(self, value):
        if not value > 1900:
            raise serializers.ValidationError(
                'The birthdate must be greater than 1900!'
            )
        return value
