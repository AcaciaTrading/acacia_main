from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^plans$', views.PlanList.as_view(), name="plan_list"),
    url(r'^upgrade/([0-9]+)/$', views.switch_plan, name="switch_plan"),
    url(r'^invoice/([0-9]+)/$', views.PayInvoice.as_view(), name="pay_invoice"),
]