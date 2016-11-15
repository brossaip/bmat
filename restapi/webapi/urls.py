from django.conf.urls import url
from webapi import views

urlpatterns = [
    url(r'^webapi/add_channel$', views.add_channel),
]
