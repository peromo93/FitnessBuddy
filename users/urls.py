# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from users import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.UserListView.as_view()),
    url(r'^create/$', views.UserCreateView.as_view()),
    url(r'^myaccount/$', views.UserDetailView.as_view()),
    url(r'^(?P<username>\w+)/$', views.ProfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
