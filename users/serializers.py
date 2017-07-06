# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User


# Create serializers here
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('pk',)
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username', 'password', 'pk')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'is_public', 'goal_calories', 'goal_fat', 'goal_carbs', 'goal_protein')
