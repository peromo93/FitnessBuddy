# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FitnessBuddy.helper import parse_date_from_url, get_profile_from_url
from foodlog.models import DailyLog, FoodEntry
from foodlog.serializers import DailyLogSerializer, FoodEntrySerializer
from users.permissions import IsOwnerOrReadOnlyIfPublic
from rest_framework import generics
from django.core import exceptions
from django.http import Http404


# Create your views here.
class DailyLogDetail(generics.RetrieveAPIView):
    """
    List all food entries for a given day
    """

    permission_classes = (IsOwnerOrReadOnlyIfPublic,)
    serializer_class = DailyLogSerializer

    def get_object(self):
        profile = get_profile_from_url(self.kwargs)
        date = parse_date_from_url(self.kwargs)

        # try to get the user's DailyLog if one exists or return empty log
        try:
            log = DailyLog.objects.get(profile=profile, date=date)
        except DailyLog.DoesNotExist:
            log = DailyLog(profile=profile, date=date)
        self.check_object_permissions(self.request, profile)
        return log


class FoodEntryCreate(generics.CreateAPIView):
    """
    Create a new food entry for a given day
    """

    serializer_class = FoodEntrySerializer

    def perform_create(self, serializer):
        profile = get_profile_from_url(self.kwargs)
        date = parse_date_from_url(self.kwargs)

        # check that current user is the owner of this log
        print self.request.user
        if self.request.user != profile.user:
            raise exceptions.PermissionDenied()

        # get validated parameters
        ndbno = serializer.validated_data.get('ndbno')
        measure = serializer.validated_data.get('measure')
        qty = float(serializer.validated_data.get('qty'))
        food_report = serializer.validated_data.get('food_report')

        # if this log does not yet exist create it
        if not DailyLog.objects.filter(profile=profile, date=date).exists():
            log = DailyLog(profile=profile, date=date)
            log.save()
        else:
            log = DailyLog.objects.get(profile=profile, date=date)

        # create a new FoodEntry
        entry = FoodEntry(daily_log=log, name=food_report.get('name'),
                          ndbno=ndbno, measure=measure, qty=qty)
        entry.fill_nutrition(food_report, measure, qty)
        entry.save()


class FoodEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, destroy a food entry
    """

    permission_classes = (IsOwnerOrReadOnlyIfPublic,)
    serializer_class = FoodEntrySerializer

    def get_object(self):
        try:
            entry = FoodEntry.objects.get(pk=self.kwargs.get('entry_pk'))
        except FoodEntry.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, entry)
        return entry

    def perform_update(self, serializer):
        entry = self.get_object()
        entry.update_quantity(serializer.validated_data.get('qty'))
        entry.save()
