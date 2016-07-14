from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^order[/]$', views.OrderTaskDetail.as_view(), name="order_detail"),
    url(r'^order/delete[/]$', views.OrderTaskDelete.as_view(), name="order_delete"),
    url(r'^orders[/]$', views.OrderTaskList.as_view(), name="order_list"),
]