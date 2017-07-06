# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions


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
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.user:
            return True
        else:
            return request.method in permissions.SAFE_METHODS and obj.is_public


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow only if not authenticated.
    This is used for creating users and logging in
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
