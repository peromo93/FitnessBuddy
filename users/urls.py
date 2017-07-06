# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from users import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.UserListView.as_view()),
    url(r'^create/$', views.UserCreateView.as_view()),
    url(r'^account/$', views.UserDetailView.as_view()),
    url(r'^profile/$', views.ProfileDetailView.as_view()),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
