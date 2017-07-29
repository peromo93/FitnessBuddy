# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from foodlog.models import FoodEntry


# Create serializers here
class MeasureTransformSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEntry
        fields = ('measure', 'calories', 'tfa', 'sfa', 'pufa',
                  'mufa', 'carb', 'fiber', 'sugar', 'protein')


class FoodTransformSerializer(serializers.Serializer):
    ndbno = serializers.CharField()                    # NDB food number
    name = serializers.CharField()                     # food name
    measures = MeasureTransformSerializer(many=True)   # food measures


class FoodSearchResultSerializer(serializers.Serializer):
    ndbno = serializers.CharField()                    # NDB food number
    name = serializers.CharField()                     # food name


class FoodSearchQuerySerializer(serializers.Serializer):
    item = FoodSearchResultSerializer(many=True)       # search results


# Old serializers
class MeasureSerializer(serializers.Serializer):
    label = serializers.CharField()            # name of measure
    eqv = serializers.FloatField()             # measure equivalent in eunits
    eunit = serializers.CharField()            # eunit of measure
    value = serializers.FloatField()           # nutrient value for measure


class NutrientSerializer(serializers.Serializer):
    nutrient_id = serializers.IntegerField()    # nutrient id
    name = serializers.CharField()              # nutrient name
    unit = serializers.CharField()              # nutrient unit
    value = serializers.FloatField()            # value for 100g
    measures = MeasureSerializer(many=True)     # food measurements


class FoodSerializer(serializers.Serializer):
    ndbno = serializers.CharField()             # NDB food number
    name = serializers.CharField()              # food name
    nutrients = NutrientSerializer(many=True)   # food nutrients
