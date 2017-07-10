# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from users.models import Profile
from foodlog.models import DailyLog, FoodEntry


# Create your permissions here
class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only account owner to access
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj


class IsOwnerOrReadOnlyIfPublic(permissions.BasePermission):
    """
    Custom permission to allow only account owner to view/update
    Provide read only access if not account owner and profile is public
    Works with Profile, DailyLog, FoodEntry objects
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Profile):
            is_public = obj.is_public
            user = obj.user
        elif isinstance(obj, DailyLog):
            is_public = obj.profile.is_public
            user = obj.profile.user
        elif isinstance(obj, FoodEntry):
            is_public = obj.daily_log.profile.is_public
            user = obj.daily_log.profile.user
        else:
            is_public = False
            user = None

        if request.user.is_authenticated and request.user == user:
            return True
        else:
            return request.method in permissions.SAFE_METHODS and is_public


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow only if not authenticated.
    This is used for creating users and logging in
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
