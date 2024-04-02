"""Сериализаторы приложения users."""
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя."""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'username',
            'id',
            'surname',
            'sex',
            'aim',
            'current_weight',
            'height',
            'birthdate',
            'activity',
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'id',
            'surname',
            'sex',
            'aim',
            'current_weight',
            'height',
            'birthdate',
            'activity',
        )
