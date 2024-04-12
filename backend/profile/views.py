from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from .models import UserProfile
from .permissions import OwnerAndAuthenticated
from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (OwnerAndAuthenticated,)
