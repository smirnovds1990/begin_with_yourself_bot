from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class FoodgramUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
