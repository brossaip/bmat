from django.conf.urls import url
from webapi import views

urlpatterns = [
    url(r'^webapi/add_channel$', views.add_channel),
    url(r'^webapi/add_performer$', views.add_channel),
    url(r'^webapi/add_song$', views.add_song),
    url(r'^webapi/add_play$', views.add_play),
]
