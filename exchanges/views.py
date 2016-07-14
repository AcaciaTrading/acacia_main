from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from abstract import Order

# Exchanges go below
from apis.btce import BTCe
from apis.bitstamp import Bitstamp
from apis.kraken import Kraken

from utils.views import *

# Create your views here.
class Exchanges(object):
    BTCE = "btc-e"
    TEST_EX = "test_ex"
    BITSTAMP = "bitstamp"
    #KRAKEN = "kraken"
    
EXCHANGE_APIS = {
    Exchanges.BTCE: BTCe(),
    Exchanges.BITSTAMP: Bitstamp()#,
    #Exchanges.KRAKEN: Kraken()
}

class ExchangeList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = [x[0] for x in EXCHANGE_APIS.items()]
        return r_success(result)


class ExchangeDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            api = get_api(request)
            result = {
                "pairs":api.PAIRS,
                "fees_cur":api.FEES_CUR,
                "fees":api.FEES,
                "order_types":api.ORDER_TYPES,
                "min_order":api.MIN_ORDER,
                "min_order_cur":api.MIN_ORDER_CUR
            }
            return r_success(result)
        except Exception as e:
            return r_failure(e)


class PairDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pair):
        try:
            api = get_api(request)
            result = api.pair_detail(pair)
            return r_success(result.data())
        except Exception as e:
            return r_failure(e)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            api = get_api(request)
            auth = get_auth(request)
            result = api.user_detail(auth)
            return r_success(result.data())
        except Exception as e:
            return r_failure(e)
        
        
class APIKeyDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            api = get_api(request)
            auth = get_auth(request)
            result = api.api_key_detail(auth)
            return r_success(result.data())
        except Exception as e:
            return r_failure(e)


class OrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            api = get_api(request)
            auth = get_auth(request)
            result = api.order_list(auth)
            orders = []
            for order in result:
                orders.append(order.data())
            return r_success(orders)
        except Exception as e:
            return r_failure(e)


class OrderDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, order_id):
        try:
            api = get_api(request)
            auth = get_auth(request)
            result = api.order_detail(int(order_id), auth)
            return r_success(result[0].data())
        except Exception as e:
            return r_failure(e)


class OrderCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            api = post_api(request)
            auth = post_auth(request)
            r = request.POST
            order = Order(
                r.get("pair"),
                r.get("order_type"),
                r.get("direction"),
                r.get("amount"),
                price=r.get("price"),
                price2=r.get("price2")
            )
            order_id = api.order_create(order, auth)
            return r_success({"order_id":order_id})
        except Exception as e:
            return r_failure(e)


class OrderDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            api = post_api(request)
            auth = post_auth(request)
            result = api.order_delete(int(request.POST.get("order_id")), auth)
            return r_success(result)
        except Exception as e:
            return r_failure(e)

def get_api(request):
    return api_from_exchange(request.GET.get("exchange"))

def post_api(request):
    return api_from_exchange(request.POST.get("exchange"))

def api_from_exchange(exchange):
    api = EXCHANGE_APIS.get(exchange)
    if api == None:
        raise InvalidExchangeError("Invalid exchange: %s" % exchange)
    return api

def get_auth(request):
    return auth_from_params(request.GET)

def post_auth(request):
    return auth_from_params(request.POST)

def auth_from_params(params):
    names = ("api_key", "api_secret", "api_id")
    auth = (
        str(params.get(names[0])),
        str(params.get(names[1])),
        str(params.get(names[2]))
    )
    for x in range(0, 2):
        if auth[x] == None:
            raise InvalidAuthError("missing parameter: " + names[x])
    return auth

class InvalidExchangeError(Exception):
    pass

class InvalidAuthError(Exception):
    pass
