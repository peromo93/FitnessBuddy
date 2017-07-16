# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FitnessBuddy.helper import get_profile_from_url
from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer
from users.permissions import IsOwner, IsOwnerOrReadOnlyIfPublic, IsNotAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class UserListView(generics.ListAPIView):
    """
    List all public users
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        profiles = Profile.objects.filter(is_public=True)
        return User.objects.filter(pk__in=profiles)


class UserCreateView(generics.CreateAPIView):
    """
    Create a new user
    """

    permission_classes = (IsNotAuthenticated,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        User.objects.create_user(**serializer.validated_data)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update username and password or delete user and user profile
    """

    permission_classes = (IsOwner,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user

    def perform_update(self, serializer):
        user = self.get_object()
        user.username = serializer.validated_data.get('username')
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        update_session_auth_hash(self.request, user)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View and update details of the user profile
    """

    permission_classes = (IsOwnerOrReadOnlyIfPublic,)
    serializer_class = ProfileSerializer

    def get_object(self):
        profile = get_profile_from_url(self.kwargs)
        self.check_object_permissions(self.request, profile)
        return profile
