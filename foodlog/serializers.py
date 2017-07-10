# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from users.serializers import ProfileSerializer
from foodlog.models import DailyLog, FoodEntry
from rest_framework import serializers
from FitnessBuddy.helper import get_food_report


# Create serializers here
class FoodEntrySerializer(serializers.ModelSerializer):

    def validate(self, data):
        ndbno = data.get('ndbno')

        # ndbno must be not None and contain only digits
        if not ndbno or not ndbno.isdigit():
            raise serializers.ValidationError(
                'ndbno must be provided as a string of only digits.')

        food_report = get_food_report(ndbno)

        # no data in USDA database for this ndbno
        if not food_report:
            raise serializers.ValidationError(
                'The ndbno provided is invalid.')

        # make sure the specified measure exists
        for measure in food_report.get('nutrients')[0].get('measures'):
            if measure.get('label') == data.get('measure'):
                data['food_report'] = food_report
                return data

        # hit this case if the measurement does not exist
        raise serializers.ValidationError(
            'The measure specified does not exist.')

    class Meta:
        model = FoodEntry
        fields = ('name', 'ndbno', 'measure', 'qty', 'calories', 'tfa', 'sfa',
                  'pufa', 'mufa', 'carb', 'fiber', 'sugar', 'protein', 'id')
        read_only_fields = ('name', 'calories', 'tfa', 'sfa', 'pufa',
                            'mufa', 'carb', 'fiber', 'sugar', 'protein', 'id')


class DailyLogSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    entries = FoodEntrySerializer(read_only=True, many=True)

    class Meta:
        model = DailyLog
        fields = ('profile', 'id', 'date', 'entries')
