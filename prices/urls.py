from django.conf.urls import include, url
from . import views

from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^prices[/]$', cache_page(30)(views.GetPrices.as_view()), name="get_prices"),
]