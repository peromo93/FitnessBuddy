# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    """
    User Profile model
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    goal_calories = models.IntegerField(default=2000)
    goal_fat = models.FloatField(default=0.3)
    goal_carbs = models.FloatField(default=0.4)
    goal_protein = models.FloatField(default=0.3)


# Function to create Profile each time a User is created
def create_profile(sender, **kwargs):
    new_user = kwargs['instance']
    if kwargs['created']:
        user_profile = Profile(user=new_user)
        user_profile.save()


# Set post_save signal on User model
post_save.connect(create_profile, sender=User)
