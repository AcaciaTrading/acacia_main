from django.test import TestCase

from billing.models import Plan, Customer, Invoice

# Create your tests here.

class PlanTestCase(TestCase):
    def test_price_string(self):
        pass
    
    def test_trade_size_string(self):
        pass
    
    
class CustomerTestCase(TestCase):
    def test_bots_below_limit(self):
        pass
    
    def test_bots_at_limit(self):
        pass
    
    def test_bots_above_limit(self):
        pass
    
    
class InvoiceTestCase(TestCase):
    def test_send_creation_email(self):
        pass
    
    def test_send_warning_email(self):
        pass
    
    def test_amount_string(self):
        pass
    
    def test_paid_string_missing(self):
        pass
    
    def test_paid_string(self):
        pass