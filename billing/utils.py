from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from billing.models import Customer, Plan

def billing_check(user):
    try:
        x = user.customer.plan
    except Customer.DoesNotExist:
        customer = Customer()
        customer.user = user
        customer.plan = Plan.objects.filter(price_cents=0)[0]
        customer.expiry_timestamp = -1
        customer.save()
    return True

class BillingCheckMixin(object):
    @method_decorator(user_passes_test(billing_check))
    def dispatch(self, *args, **kwargs):
        return super(BillingCheckMixin, self).dispatch(*args, **kwargs)