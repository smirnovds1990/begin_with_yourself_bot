from datetime import date

from profile.models import UserProfile

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import (ACTIVITY_MODIFIERS,
                        GENDER_MODIFIERS,
                        GOAL_MODIFIERS)


class CalorieNormView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        current_year = date.today().year
        age = current_year - profile.birthdate

        gender_factors = GENDER_MODIFIERS[profile.sex]
        calories = (
            gender_factors['base'] +
            (gender_factors['weight'] * profile.current_weight) +
            (gender_factors['height'] * profile.height) -
            (gender_factors['age'] * age)
        )

        activity_modifier = ACTIVITY_MODIFIERS[profile.activity]
        goal_modifier = GOAL_MODIFIERS[profile.aim]

        calories *= activity_modifier
        calories *= goal_modifier

        return Response({'calories_norm': calories})
