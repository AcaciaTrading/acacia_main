from django.conf.urls import include, url
from . import views

from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^exchanges[/]$', cache_page(60 * 15)(views.ExchangeList.as_view()), name="exchange_list"),
    url(r'^exchange[/]?$', cache_page(60 * 15)(views.ExchangeDetail.as_view()), name="exchange_detail"),
    url(r'^pairs/([\w-]+)[/]?$', cache_page(5)(views.PairDetail.as_view()), name="pair_detail"),
    url(r'^user[/]?$', views.UserDetail.as_view(), name="user_detail"),
    url(r'^api_key[/]?$', views.APIKeyDetail.as_view(), name="api_key_detail"),
    url(r'^orders[/]?$', views.OrderList.as_view(), name="order_list"),
    url(r'^orders/([0-9]+)[/]?$', views.OrderDetail.as_view(), name="order_detail"),
    url(r'^order/create[/]$', views.OrderCreate.as_view(), name="order_create"),
    url(r'^order/delete[/]$', views.OrderDelete.as_view(), name="order_delete"),
    #url(r'^api/v1/resource/(?P<resource_id>\d+)[/]?$', login_required(MyRESTView.as_view()), name='my_rest_view'),
    #url(r'^api/v1/resource[/]?$', login_required(MyRESTView.as_view()), name='my_rest_view'),
]