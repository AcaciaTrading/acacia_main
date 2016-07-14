from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from trades.models import OrderTask

from utils.views import *
from utils.client import auth_from_order
from utils.convert import cur_convert

from exchanges.views import EXCHANGE_APIS
from exchanges.abstract import APIKey

import time

# Create your views here.
class OrderTaskDetail(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            result = request.user.order_tasks.get(pk=request.GET["order_id"])
            return r_success(result.json_fields())
        except Exception:
            return r_failure("Invalid order_id.")
    
    def post(self, request):
        missing = missing_params(request.POST, OrderTask.REQUIRED_FIELDS)
        if len(missing) == 0:
            try:
                check_keys(request)
            except Exception as e:
                return r_failure(str(e))
            
            try:
                check_params(request)
            except Exception as e:
                return r_failure(str(e))
            
            new_order = OrderTask()
            new_order.user = request.user
            
            for field in OrderTask.REQUIRED_FIELDS:
                setattr(new_order, field, request.POST[field])
                
            if request.POST.get("api_id"):
                new_order.api_id = request.POST["api_id"]
            
            if request.POST.get("amount"):
                new_order.amount = float(request.POST["amount"])
                new_order.amount_remaining = float(request.POST["amount"])
            else:
                fill_order_amount(new_order)
            
            new_order.start_timestamp = int(time.time())
            new_order.deadline_timestamp = \
                int(time.time()) + int(request.POST["time"])
            
            new_order.total_trades = calc_total_trades(new_order)
            
            new_order.save()
            print "now:", time.time(), "start", new_order.start_timestamp
            print "end:", new_order.deadline_timestamp
            print "total: ", new_order.total_trades
            return r_success(new_order.pk)
        else:
            return r_failure("Missing parameter(s): %s" % ", ".join(missing))
        
        
class OrderTaskList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        result = request.user.order_tasks.all()
        result = [x.json_fields() for x in list(result)]
        return r_success(result)
    
    
class OrderTaskDelete(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            result = request.user.order_tasks.get(pk=request.POST["order_id"])
            result.delete()
            return r_success("Order successfully deleted.")
        except Exception:
            return r_failure("Invalid order_id.")
    
    
def missing_params(request_params, params):
    missing = []
    for param in params:
        if request_params.get(param) == None:
            missing.append(param)
    return missing

def check_keys(request):
    ex = EXCHANGE_APIS[request.POST["exchange"]]
    p = ex.api_key_detail(
        (
            str(request.POST["api_key"]),
            str(request.POST["api_secret"]),
            str(request.POST.get("api_id")),
        )
    ).permissions
    
    if p[APIKey.USER_BALANCES] == 0 or p[APIKey.ORDER_CREATE] == 0:
        raise BadKeysException(
            "API Keys must have 'user balance' and 'create order' permissions"
        )
        
def check_params(request):
    errors = []
    if int(request.POST["time"]) < 300 or int(request.POST["time"]) > 21600:
        errors.append(
            "'time' parameter must be between 300 (5 min) and 21600 (6 hours)"
        )
        
    if request.POST.get("amount"):
        amount = float(request.POST["amount"])
        if amount < 0:
            errors.append("'amount' parameter must be positive")
            
    if request.POST["direction"] not in (
        OrderTask.DIRECTION_BUY,
        OrderTask.DIRECTION_SELL
    ):
        errors.append(
            "'direction' parameter must be either '%s' or '%s'" % (
                OrderTask.DIRECTION_BUY, OrderTask.DIRECTION_SELL
            )
        )
    
    if len(errors) > 0:
        raise BadParamsException(",".join(errors))
        
def fill_order_amount(order, p_reserve=0.0, s_reserve=0.0):
    ex = EXCHANGE_APIS[order.exchange]
    balances = ex.user_detail(auth_from_order(order)).balances
    #print balances
    
    curs = split_trading_pair(order.trading_pair)
    if order.direction == OrderTask.DIRECTION_SELL:
        order.amount = order.amount_remaining = max(0, balances[curs[0]] - s_reserve)
    else:
        order.amount = order.amount_remaining = max(0, balances[curs[1]] - p_reserve)
    #print order.amount, order.amount_remaining
    order.autofilled = True
            
def split_trading_pair(pair):
    return (pair[:pair.index("_")], pair[pair.index("_") + 1:],)
            
def calc_total_trades(order):
    min_order_amount = calc_min_order_amount(order)
    time_remaining = order.deadline_timestamp - order.start_timestamp
    
    return int(min(
        (1.0 * time_remaining / order.MIN_ORDER_INTERVAL),
        (1.0 * order.amount / min_order_amount)
    ))

def calc_min_order_amount(order):
    ex = EXCHANGE_APIS[order.exchange]
    
    order_curs = split_trading_pair(order.trading_pair)
    if not order.autofilled or order.direction == OrderTask.DIRECTION_SELL:
        order_cur = order_curs[0]
    else:
        order_cur = order_curs[1]
        
    min_amount = cur_convert(
        ex.MIN_ORDER, ex.MIN_ORDER_CUR,
        order_cur, ex.PAIRS, order
    )
    
    if order.user.customer.plan.max_trade_size_usd == -1.0:
        return min_amount
    else:
        return min(
            min_amount,
            cur_convert(
                order.user.customer.plan.max_trade_size_usd, "usd",
                order_cur, ex.PAIRS, order
            )
        )
    
    
class BadKeysException(Exception):
    pass

class BadParamsException(Exception):
    pass