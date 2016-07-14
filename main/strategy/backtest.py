from prices.interface import prices_get
from main.strategy.evaluate import evaluate_strategy
from trades.models import OrderTask

import time
import datetime

# 48h of price data to be safe
PRICES_BUFFER = 2880

def run_backtest(backtest, trim=False):
    # THIS NEEDS ERROR CATCHING / TESTING => should report to backtest method
    prices = prices_get(backtest.exchange, backtest.trading_pair)
    
    current_time = int(time.time())
    start_index = (current_time - backtest.timestamp_start) / 60
    end_index = (current_time - backtest.timestamp_end) / 60
    print start_index, end_index
    
    adjusted_prices = prices[end_index:(start_index + PRICES_BUFFER)]
    if len(adjusted_prices) < (start_index + PRICES_BUFFER - end_index):
        if not trim:
            raise Exception("Not enough price data for specified bounds.")
        else:
            start_index = len(adjusted_prices) - PRICES_BUFFER + end_index
            backtest.timestamp_start = current_time - (60 * start_index)
            backtest.save()
            print "start to", start_index
    
    strat = backtest.strategy
    price_ratio = strat.time_interval / 60
    
    previous_position = OrderTask.DIRECTION_SELL
    trades = []
    for index in range(start_index - end_index, 0, -1):
        evaluate_prices = adjusted_prices[index:][0::price_ratio]
        position = evaluate_strategy(
            strat,
            backtest.exchange,
            backtest.trading_pair,
            prices=evaluate_prices
        )
        
        if (position == OrderTask.DIRECTION_BUY or position == OrderTask.DIRECTION_SELL) and position != previous_position:
            date = datetime.datetime.fromtimestamp(
                backtest.timestamp_start + (60 * (start_index - end_index -index))
            ).strftime('%b %-d at %-I:%M %p')
            trades.append({
                "date": str(date),
                "type": position,
                "price": evaluate_prices[0]
            })
            previous_position = position
            
    amt_primary_start = 100.0
    amt_secondary_start = amt_primary_start / prices[min(len(prices) - 1, start_index)]
    print amt_primary_start, amt_secondary_start
    
    amount = amt_primary_start
    is_primary = True
    for i in range(0, len(trades)):
        if i % 2 == 0:
            amount /= trades[i]["price"]
            trades[i]["amount"] = round(10000.0 * amount) / 10000
            is_primary = False
        else:
            trades[i]["amount"] = round(10000.0 * amount) / 10000
            amount *= trades[i]["price"]
            is_primary = True
            
    if is_primary:
        amt_primary = amount
        amt_secondary = amount / prices[0]
    else:
        amt_primary = amount * prices[0]
        amt_secondary = amount
        
    backtest.profit_primary = round(10000.0 * (amt_primary - amt_primary_start) / amt_primary_start) / 100.0
    backtest.profit_secondary = round(10000.0 * (amt_secondary - amt_secondary_start) / amt_secondary_start) / 100.0
    backtest.done = True
    backtest.save()
    print trades, amt_primary, amt_secondary
    return trades