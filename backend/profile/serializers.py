from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
        optional = [
            'aim',
            'activity'
        ]

    def validate(self, data):
        if not data['current_weight'] > 0:
            raise serializers.ValidationError(
                "current_weight must be greater than zero!"
            )
        if not data['height'] > 0:
            raise serializers.ValidationError(
                "height must be greater than zero!"
            )
        if not data['birthdate'] > 1900:
            raise serializers.ValidationError(
                "birthdate must be greater than 1900!"
            )
        if data['user'] != self.context['request'].user:
            raise serializers.ValidationError(
                "You cannot create on behalf of someone else!"
            )
        return data
