from django.test import TestCase
from ddt import ddt, data

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from utils.auth_tokens import new_auth_token

from exchanges import views

import json
import time

# import API Keys (local file)
from keys import KEYS

# Create your tests here.
EXCHANGES = [x for x in views.EXCHANGE_APIS]
EXCHANGE = "btc-e"

AUTH_TOKEN = ""

class BadExchangeTestCase(TestCase):
    def test_missing_exchange(self):
        """When there is no 'exchange' parameter, an error should
        be returned.
        """
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            '{"success":false,"error":"Invalid exchange: None"}'
        )
        
    def test_invalid_exchange(self):
        """When the 'exchange' parameter is invalid, an error should
        be returned.
        """
        invalid_exchange = "24g2g4gwe"
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            {"exchange":invalid_exchange},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            '{"success":false,"error":"Invalid exchange: %s"}' \
                % invalid_exchange
        )
        
    def test_valid_exchange(self):
        """When the 'exchange' parameter is correct, the request should return
        a normal response.
        """
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            {"exchange":EXCHANGE},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["success"])
        
        
class BadAuthTokenTestCase(TestCase):
    def test_missing_auth(self):
        """If an API method is called without the authorization header, an
        error should be returned.
        """
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            {"exchange":EXCHANGE}
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content,
            '{"detail":"Authentication credentials were not provided."}'
        )
        
    def test_bad_auth(self):
        """If an API method is called with an invalid authorization header, an
        error should be returned.
        """
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            {"exchange":EXCHANGE},
            HTTP_AUTHORIZATION="Token blahblahblah"
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, '{"detail":"Invalid token."}')
        
        
class ExchangeListTestCase(TestCase):
    def test_success(self):
        """When exchange_list is called, it should return a list of the valid
        exchanges to use.
        """
        response = self.client.get(
            reverse("exchanges:exchange_list"),
            HTTP_AUTHORIZATION=new_auth_token()
        )
        ideal_response = {
            "success": True,
            "result": ["bitstamp", "btc-e"]
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), ideal_response)
        
        
@ddt
class ExchangeDetailTestCase(TestCase):
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When exchange_detail is called, it should return informaiton about
        the given exchange.
        """
        response = self.client.get(
            reverse("exchanges:exchange_detail"),
            {"exchange":exchange},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(result["result"]["pairs"]) is list or type(result["result"]["pairs"]) is unicode)
        
        self.assertTrue(type(result["result"]["min_order"]) is float)
        self.assertTrue(type(result["result"]["min_order_cur"]) is unicode)
        
        self.assertTrue(type(result["result"]["fees"]) is list)
        self.assertTrue(type(result["result"]["fees"][0]) is dict)
        self.assertTrue(type(result["result"]["fees_cur"]) is unicode)
        
        
@ddt
class PairDetailTestCase(TestCase):
    @data(*EXCHANGES)
    def test_invalid_pair(self, exchange):
        """When the 'pair' parameter is invalid, an error should
        be returned.
        """
        invalid_pair = "rg3oirg3o"
        response = self.client.get(
            reverse("exchanges:pair_detail", args=[invalid_pair]),
            {"exchange":exchange},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            '{"success":false,"error":"Invalid pair name: %s"}' % invalid_pair
        )
        
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When pair_detail is called, it should return information about the
        specific trading pair.
        """
        valid_pair = "btc_usd"
        response = self.client.get(
            reverse("exchanges:pair_detail", args=[valid_pair]),
            {"exchange":exchange},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        result = json.loads(response.content)
        
        self.assertTrue(result["success"])
        result = result["result"]
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(result["ticker"]) is dict)
        self.assertTrue(type(result["ticker"]["low"]) is float)
        self.assertTrue(type(result["volume"]) is float)
        self.assertTrue(type(result["depth"]) is dict)
        self.assertTrue(type(result["fees"]) is list)
        
        
@ddt
class UserDetailTestCase(TestCase):
    @data(*EXCHANGES)
    def test_missing_auth(self, exchange):
        """When an authenticated method is called without authentication, an
        error should be returned.
        """
        response = self.client.get(
            reverse("exchanges:user_detail"),
            {"exchange":exchange},
            HTTP_AUTHORIZATION=new_auth_token()
        )
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["success"], False)
        
    @data(*EXCHANGES)
    def test_bad_auth(self, exchange):
        """When an invalid API key and/or is supplied, an error should
        be returned.
        """ 
        auth = ("eg34g34g", "24vb998h3", 292832)
        response = auth_get(self, "exchanges:user_detail", {"exchange":exchange}, auth)
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["success"], False)
    
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When the user detail method is called with correct authentication
        and params, the user's balances and trades should be returned.
        """
        auth = KEYS[exchange]
        response = auth_get(self, "exchanges:user_detail", {"exchange":exchange}, auth)
        result = json.loads(response.content)
        
        if response.status_code != 200:
            print "\n", response.content
        self.assertEqual(response.status_code, 200)
        result = result["result"]
        
        self.assertTrue(type(result["trades"]) is list)
        self.assertTrue(type(result["balances"]) is dict)
        
        for trade in result["trades"]:
            self.assertTrue(type(trade["pair"]) is unicode)
            self.assertTrue(type(trade["order_type"]) is unicode)
            self.assertTrue(type(trade["timestamp"]) is int)

            self.assertTrue(type(trade["price"]) is float or type(trade["price"]) is int)
            self.assertTrue(type(trade["amount"]) is float)
        
        for currency, amount in result["balances"].items():
            self.assertTrue(type(currency) is unicode)
            self.assertTrue(type(amount) is float)
            
            
@ddt
class APIKeyDetailTestCase(TestCase):
    def setUp(self):
        time.sleep(1)
        
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When the API key detail method is called with the correct
        authentication (as tested in the UserDetailTestCase), the permissions
        of the API key pair should be returned.
        """
        auth = KEYS[exchange]
        response = auth_get(self, "exchanges:api_key_detail", {"exchange":exchange}, auth)
        result = json.loads(response.content)
        
        if response.status_code != 200:
            print "\n", response.content
        self.assertEqual(response.status_code, 200)
        result = result["result"]["permissions"]
        
        for permission, num in result.items():
            self.assertTrue(type(permission) is unicode)
            self.assertTrue(type(num) is int)
            self.assertTrue(num == 0 or num == 1)
            
            
@ddt
class OrderCreateDeleteTestCase(TestCase):
    def setUp(self):
        time.sleep(2)
        
    @data(*EXCHANGES)
    def test_bad_order_type(self, exchange):
        """When an invalid order type is specified, an error should
        be returned.
        """
        auth = KEYS[exchange]
        
        response = order_request(self, exchange, auth, order_type="434g3")
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["success"], False)
        
    @data(*EXCHANGES)
    def test_missing_order_type(self, exchange):
        """When a parameter is missing (like order_type), an error should
        be returned.
        """
        auth = KEYS[exchange]
        
        response = order_request(self, exchange, auth, order_type=None)
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["success"], False)
        
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When the order_create and order_delete methods are called with
        valid parameters, the order_id should be returned when an order is
        created and null should be returned when it's deleted.
        """
        auth = KEYS[exchange]
        
        order_id = create_sample_order(self, exchange, auth)
        cancel_order(self, exchange, order_id, auth)
        
        
@ddt
class OrderListTestCase(TestCase):
    def setUp(self):
        time.sleep(1)
        
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When the order_list method is called with valid authentication,
        a list of the current active orders on a given exchange should
        be returned.
        """
        auth = KEYS[exchange]
        
        order_id = create_sample_order(self, exchange, auth)
        response = auth_get(self, "exchanges:order_list", {"exchange":exchange}, auth)
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        result = result["result"]
        for order in result:
            self.assertTrue(order["direction"] in ("buy", "sell"))
            self.assertTrue(type(order["order_type"]) is unicode)
            self.assertTrue(type(order["order_id"]) is int)
            self.assertTrue(type(order["price"]) is float)
            self.assertTrue(type(order["amount"]) is float)
            self.assertTrue(type(order["pair"]) is unicode)
            
            if order["order_id"] == order_id:
                self.assertEqual(order["pair"], "btc_usd")
                self.assertEqual(order["price"], 50)
                self.assertEqual(order["amount"], 0.1)
                self.assertEqual(order["direction"], "buy")
                
        cancel_order(self, exchange, order_id, auth)
        
        
@ddt
class OrderDetailTestCase(TestCase):
    def setUp(self):
        time.sleep(1)
        
    @data(*EXCHANGES)
    def test_success(self, exchange):
        """When the order_detail method is called with valid parameters,
        the details of the given order should be returned.
        """
        auth = KEYS[exchange]
        
        order_id = create_sample_order(self, exchange, auth)
        response = auth_get(self, "exchanges:order_detail", {"exchange":exchange}, auth, args=(order_id,))
        cancel_order(self, exchange, order_id, auth)
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        result = result["result"]
        
        self.assertTrue(result["direction"] in ("buy", "sell"))
        self.assertTrue(result["order_id"] == order_id)
        
        self.assertTrue(type(result["order_type"]) is unicode)
        self.assertTrue(type(result["order_id"]) is int)
        self.assertTrue(type(result["price"]) is float)
        self.assertTrue(type(result["amount"]) is float)
        self.assertTrue(type(result["amount_remaining"]) is float)
        self.assertTrue(type(result["pair"]) is unicode)
        
        
def create_sample_order(self, exchange, auth):
    response = order_request(self, exchange, auth)
    result = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    result = result["result"]

    self.assertTrue(type(result["order_id"]) is int)
    return result["order_id"]

def order_request(self, exchange, auth, pair="btc_usd", order_type="limit", price="50", amount=0.1, direction="buy"):
    return auth_post(
        self,
        "exchanges:order_create",
        {
            "exchange":exchange,
            "pair":pair,
            "order_type":order_type,
            "price":price,
            "amount":amount,
            "direction":direction
        },
        auth
    )
        

def cancel_order(self, exchange, order_id, auth):
    response = auth_post(
        self,
        "exchanges:order_delete",
        {
            "exchange":exchange,
            "order_id":order_id
        },
        auth
    )
    
    self.assertEqual(response.status_code, 200)
    result = json.loads(response.content)
    
    self.assertEqual(result["result"], None)

def auth_get(self, url, params, auth, args=None, auth_token=None):
    return auth_request(url, params, auth, self.client.get, args=args, auth_token=auth_token)

def auth_post(self, url, params, auth):
    return auth_request(url, params, auth, self.client.post)

def auth_request(url, params, auth, method, args=None, auth_token=None):
    params["api_key"] = auth[0]
    params["api_secret"] = auth[1]
    try:
        params["api_id"] = auth[2]
    except IndexError:
        pass
    
    if auth_token == None:
        auth_token = new_auth_token()
    
    response = method(reverse(url, args=args), params, HTTP_AUTHORIZATION=auth_token)
    return response