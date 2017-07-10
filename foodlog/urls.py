# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from foodlog import views


urlpatterns = [
    url(r'^(?P<username>\w+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<year>[0-9]+)/$', views.DailyLogDetail.as_view()),
    url(r'^(?P<username>\w+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<year>[0-9]+)/create/$', views.FoodEntryCreate.as_view()),
    url(r'^entry/(?P<entry_pk>[0-9]+)/$', views.FoodEntryDetail.as_view()),
]
