from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^username/$', views.username, name="username"),
    url(r'^profile/$', views.profile_redirect, name="profile_redirect"),
]