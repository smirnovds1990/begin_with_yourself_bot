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
            'aim',
            'activity'
        ]
