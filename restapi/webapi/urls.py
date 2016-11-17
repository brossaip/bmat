# coding: utf-8

from django.conf.urls import url
from webapi import views

reg_exp_data = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'

urlpatterns = [
    url(r'^webapi/add_channel$', views.add_channel),
    url(r'^webapi/add_performer$', views.add_channel),
    url(r'^webapi/add_song$', views.add_song),
    url(r'^webapi/add_play$', views.add_play),
    url(r'^webapi/get_song_plays/(?P<title>.*)/(?P<performer>.*)/(?P<start>'
        + reg_exp_data + ')/(?P<end>' + reg_exp_data + ')$', views.get_song_plays),
    url(r'^webapi/get_channel_plays/(?P<channel>.*)/(?P<start>' + reg_exp_data
        + ')/(?P<end>' + reg_exp_data + ')$', views.get_channel_plays),
    url(r'^webapi/get_top/(?P<channel>.*)/(?P<start>' + reg_exp_data
        + ')/(?P<limit>[0-9]+)$', views.get_top),
]
