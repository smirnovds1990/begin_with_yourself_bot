from rest_framework import serializers
from .models import (WorkoutType,
                     WorkoutProgram,
                     WorkoutProgramDetail)


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


class WorkoutProgramDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    workout_title = serializers.CharField(
        source='workout.title'
    )

    class Meta:
        model = WorkoutProgramDetail
        fields = (
            'name',
            'workout_title',
            'order',
            'repetitions',
            'sets',
            'duration'
        )

    def get_name(self, obj):
        return str(obj)


class WorkoutProgramSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    program_details = WorkoutProgramDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = WorkoutProgram
        fields = (
            'id',
            'sex',
            'aim',
            'name',
            'program_details'
        )

    def get_name(self, obj):
        return str(obj)
