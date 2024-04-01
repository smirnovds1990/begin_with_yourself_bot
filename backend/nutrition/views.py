from datetime import date

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from profile.models import UserProfile

from .constants import (ACTIVITY_MODIFIERS,
                        GENDER_MODIFIERS,
                        GOAL_MODIFIERS)


@login_required
def calorie_norm(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    current_year = date.today().year
    age = current_year - profile.year_of_birth

    gender_factors = GENDER_MODIFIERS[profile.gender]
    calories = (
            gender_factors['base'] +
            (gender_factors['weight'] * profile.current_weight) +
            (gender_factors['height'] * profile.height) -
            (gender_factors['age'] * age)
            )

    calories *= ACTIVITY_MODIFIERS[profile.activity_level]
    calories *= GOAL_MODIFIERS[profile.goal]

    return HttpResponse(
        f'Ваша норма калорий: {calories:.2f}'
        )
