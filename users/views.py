# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer
from users.permissions import IsOwner, IsOwnerOrReadOnlyIfPublic, IsNotAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.http import Http404


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
        obj = None
        if self.kwargs.get('pk'):
            obj = get_object_or_404(Profile, user__pk=self.kwargs.get('pk'))
        elif self.request.user.is_authenticated:
            obj = get_object_or_404(Profile, user=self.request.user)
        else:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj
