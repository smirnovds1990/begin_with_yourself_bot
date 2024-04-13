from rest_framework import serializers
from .models import (Workout,
                     WorkoutType,
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
    workout_id = serializers.IntegerField(
        source='workout.id',
        read_only=True
    )
    workout_title = serializers.CharField(
        source='workout.title',
        read_only=True
    )

    class Meta:
        model = WorkoutProgramDetail
        fields = (
            'name',
            'workout_id',
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
    program_details = serializers.SerializerMethodField()

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

    def get_program_details(self, obj):
        """
        Получает детали программы тренировок с учётом фильтров,
        заданных через контекст.
        """
        filters = {}
        if self.context.get('filter_active', False):
            filters['workout__workout_type__is_active'] = True
        workout_type_id = self.context.get(
            'workout_type_id'
        )
        if workout_type_id is not None:
            filters['workout__workout_type_id'] = workout_type_id

        details = obj.program_details.filter(
            **filters
        )

        return WorkoutProgramDetailSerializer(
            details,
            many=True
        ).data


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
