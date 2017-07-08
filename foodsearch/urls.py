# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from foodsearch import views


urlpatterns = [
    url(r'^list/$', views.FoodSearchQuery.as_view()),
    url(r'^detail/$', views.FoodDetail.as_view()),
]
