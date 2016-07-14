from django.test import TestCase

# Create your tests here.

class PlanListTestCase(TestCase):
    def test_success(self):
        pass
    
    
class IndexViewTestCase(TestCase):
    def test_no_invoices(self):
        pass
    
    def test_success(self):
        pass
    
    
class PayInvoiceGetTestCase(TestCase):
    def test_missing_param(self):
        pass
    
    def test_bad_id(self):
        pass
    
    def test_paid_invoice(self):
        pass
    
    def test_success(self):
        pass
    
    
class PayInvoicePostTestCase(TestCase):
    def test_missing_params(self):
        pass
    
    def test_bad_id(self):
        pass
    
    def test_paid_invoice(self):
        pass
    
    def test_bad_stripe_id(self):
        pass
    
    def test_bad_bitcoin_payment(self):
        pass
    
    def test_bitcoin_payment(self):
        pass
    
    def test_bad_card_payment(self):
        pass
    
    def test_card_payment(self):
        pass
    
    
class SwitchPlanTestCase(TestCase):
    def test_missing_plan_id(self):
        pass
    
    def test_invalid_plan_id(self):
        pass
    
    def test_current_plan_id(self):
        pass
    
    def test_success_downgrade(self):
        pass
    
    def test_success_downgrade_to_free(self):
        pass
    
    def test_success_upgrade(self):
        pass
    
    
class SwitchPlanGetTestCase(TestCase):
    def test_missing_stripe_id(self):
        pass
    
    def test_bad_stripe_id(self):
        pass
    
    def test_success(self):
        pass
    
    
class SwitchPlanPostTestCase(TestCase):
    def test_missing_stripe_params(self):
        pass
    
    def test_bad_stripe_params(self):
        pass
    
    def test_bad_bitcoin_payment(self):
        pass
    
    def test_bitcoin_payment(self):
        pass
    
    def test_bad_card_payment(self):
        pass
    
    def test_card_payment(self):
        pass