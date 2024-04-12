from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
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

    def validate(self, data):
        if not data['current_weight'] > 0:
            raise serializers.ValidationError(
                "current_weight must be more zero"
            )
        if not data['height'] > 0:
            raise serializers.ValidationError(
                "height must be more zero"
            )
        if not data['birthdate'] > 1900:
            raise serializers.ValidationError(
                "birthdate must be more 1900"
            )
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        if get_object_or_404(UserProfile, user=request.user.id):
            raise serializers.ValidationError(
                "You already have a user!"
            )
        if request:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError(
                "You have not user!"
            )
        return UserProfile.objects.create(**validated_data)
