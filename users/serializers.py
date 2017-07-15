# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


# Create serializers here
class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # create User instance and get password
        user = User(**data)
        password = data.get('password')

        # validate password and raise errors if password is invalid
        errors = {}
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        # continue with validation
        return super(UserSerializer, self).validate(data)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username', 'password', 'pk')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'is_public', 'goal_calories',
                  'goal_fat', 'goal_carbs', 'goal_protein')
