# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import Profile
from FitnessBuddy.helper import nutrient_lookup, nutrient_name_list


# Create your models here.
class DailyLog(models.Model):
    """
    Food log for a single day
    """

    profile = models.ForeignKey(
        Profile, unique_for_date='date', on_delete=models.CASCADE)
    date = models.DateField(blank=False)


class FoodEntry(models.Model):
    """
    A single food entry
    """

    daily_log = models.ForeignKey(
        DailyLog, related_name='entries', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    ndbno = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    qty = models.FloatField()
    calories = models.IntegerField()
    tfa = models.FloatField(blank=True, null=True)
    sfa = models.FloatField(blank=True, null=True)
    pufa = models.FloatField(blank=True, null=True)
    mufa = models.FloatField(blank=True, null=True)
    carb = models.FloatField(blank=True, null=True)
    fiber = models.FloatField(blank=True, null=True)
    sugar = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)

    def fill_nutrition(self, food_report, measure, qty):
        """
        Fill model fields with nutrition information from food report
        """

        for nutrient in food_report.get('nutrients'):
            nutrient_id = nutrient.get('nutrient_id')
            for food_measure in nutrient.get('measures'):
                if food_measure.get('label') == measure:
                    self.__dict__[nutrient_lookup.get(nutrient_id)] = (
                        float(food_measure.get('value')) * qty)

    def update_quantity(self, new_qty):
        """
        Update nutrition based on new quantity
        """

        for nutrient in nutrient_name_list:
            self.__dict__[nutrient] *= (new_qty / self.qty)

        self.qty = new_qty
