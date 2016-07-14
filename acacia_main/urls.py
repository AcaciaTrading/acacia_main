"""acacia_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Users
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('user_sessions.urls', namespace='user_sessions')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/', include('users.urls', namespace="users")),
    
    # Exchange API
    url(r'^exchanges/', include('exchanges.urls', namespace="exchanges")),
    url(r'^exchanges/', include('exchanges_website.urls', namespace="exchanges_website")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Trades API
    url(r'^trades/', include('trades.urls', namespace="trades")),
    
    # Prices API
    url(r'^prices/', include('prices.urls', namespace="prices")),
    
    # Main Site (should eventually change to root url)
    url(r'', include('main.urls', namespace="main")),
    
    # Billing App
    url(r'^billing/', include('billing.urls', namespace="billing")),
    
    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
]