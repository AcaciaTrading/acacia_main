from django.test import TestCase

from django.core.urlresolvers import reverse

from utils.auth_tokens import new_auth_token

import json

# Create your tests here.
class GetPricesTestCase(TestCase):
    def test_missing_exchange(self):
        """When there is no 'exchange' parameter, an error should
        be returned.
        """
        response = self.client.get(
            reverse("prices:get_prices"),
            {"pair":"btc_usd"},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Exchange/trading pair combination not found."
        )
        
    def test_missing_exchange(self):
        """When there is no 'pair' parameter, an error should
        be returned.
        """
        response = self.client.get(
            reverse("prices:get_prices"),
            {"exchange":"btc-e"},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Must specify 'exchange' and 'pair' parameters."
        )
        
    def test_bad_params(self):
        """When an invalid combination of exchange / pair params is supplied,
        an error should be returned.
        """
        response = self.client.get(
            reverse("prices:get_prices"),
            {"exchange":"btc-e", "pair":"349g4ubfref"},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Exchange/trading pair combination not found."
        )
        
    def test_success(self):
        """When all params are correct, a list of prices should
        be returned.
        """
        response = self.client.get(
            reverse("prices:get_prices"),
            {"exchange":"btc-e", "pair":"btc_usd"},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        for price in result["result"]:
            self.assertTrue(type(price) is int or type(price) is float)
            
    def test_limit_days(self):
        """When all params are correct and 'days' is specified,a limited
        number of prices should be returned.
        """
        response = self.client.get(
            reverse("prices:get_prices"),
            {"exchange":"btc-e", "pair":"btc_usd", "days":1},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(len(result["result"]) <= 1440)