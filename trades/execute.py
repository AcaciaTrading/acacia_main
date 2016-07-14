import time
import threading
import math

from utils.client import auth_from_order
from trades.models import OrderTask

from exchanges.views import EXCHANGE_APIS
from exchanges.abstract import Order

from main.models import BotTrade
    
def execute_trade(order):
    # ISSUE: this is messing with the nonces when there are parallel requests with the same api keys
    # ISSUE: make sure that 'autofilled' is factored in => affects what trade amount to calculate
    #balances = api_get("exchanges:user_detail", order.user.auth_token.key, order_params(order))["result"]["balances"]
    print order.total_trades, order.trades_made
    try:
        trade_amount = 1.0 * order.amount_remaining / (order.total_trades - order.trades_made)
    except ZeroDivisionError:
        return
    
    ex = EXCHANGE_APIS[order.exchange]
    ticker = ex.pair_ticker(order.trading_pair)
    
    if order.autofilled and order.direction == OrderTask.DIRECTION_BUY:
        trade_amount = 0.98 * trade_amount / ticker.ask
    
    if order.direction == OrderTask.DIRECTION_BUY:
        price = 1.02 * ticker.ask
    else:
        price = 0.98 * ticker.bid
        
    api_order = Order(
        order.trading_pair,
        Order.LIMIT_ORDER,
        order.direction,
        floor_amount(trade_amount),
        price=round_figures(price, 5)
    )
    order_id = ex.order_create(api_order, auth_from_order(order))
    print order_id
    order.trades_made += 1
    order.save()

def batch_execute(orders):
    for order in orders:
        thr = threading.Thread(target=execute_trade, args=(order,), kwargs={})
        thr.start()
        
        
def round_figures(x, n):
    """Returns x rounded to n significant figures.
    from https://mail.python.org/pipermail/tutor/2009-September/071393.html
    """
    return round(x, int(n - math.ceil(math.log10(abs(x)))))

def floor_amount(x):
    """Returns x floored to n significant figures.
    from https://mail.python.org/pipermail/tutor/2009-September/071393.html
    """
    factor = 1000000
    return 1.0 * int(x * factor) / factor