from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileView(APIView):

    def post(self, request):
        user_create = request.user
        if UserProfile.objects.filter(user=user_create).first():
            request.data['message'] = 'Такой объект уже существует!'
            return Response(request.data, status=status.HTTP_409_CONFLICT)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user_create
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userprofile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        userprofile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(
            userprofile,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.data['message'] = 'Что-то пошло не так!'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        userprofile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(
            instance=userprofile,
            data=request.data,
            partial=True
        )
        print(f'serializer.instance = {serializer.instance}')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.data['message'] = 'Что-то пошло не так!'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
