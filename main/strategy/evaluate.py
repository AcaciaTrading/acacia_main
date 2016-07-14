from django.core.exceptions import ObjectDoesNotExist

from main.strategy.indicators import AVERAGE_METHODS, INDICATOR_METHODS
from trades.models import OrderTask

from prices.interface import prices_get

def evaluate_strategy(strategy, exchange, trading_pair, prices=None):
    if prices == None:
        price_ratio = strategy.time_interval / 60
        prices = prices_get(
            exchange,
            trading_pair,
            num_prices=3600 / price_ratio,
            price_ratio=price_ratio
        )
    
    net_signals = 0
    for i in strategy.indicators.all():
        value = INDICATOR_METHODS[i.indicator_type](prices)
        
        if i.buy_threshold >= i.sell_threshold:
            if value > i.buy_threshold:
                net_signals += 1
            elif value < i.sell_threshold:
                net_signals -= 1
        else:
            if value < i.buy_threshold:
                net_signals += -1
            elif value > i.sell_threshold:
                net_signals -= 1
    try:
        if strategy.average_crossover != None:
            c = strategy.average_crossover
            
            first_value = AVERAGE_METHODS[c.first_type](prices, c.first_interval)
            second_value = AVERAGE_METHODS[c.second_type](prices, c.second_interval)
            difference = 100.0 * (first_value - second_value) / second_value
            
            if difference > c.buy_threshold:
                net_signals += 1
            elif difference < -1 * c.sell_threshold:
                net_signals -= 1
                
    except ObjectDoesNotExist:
        pass
        
    if net_signals >= strategy.buy_triggers_required:
        return OrderTask.DIRECTION_BUY
    elif net_signals <= -1 * strategy.sell_triggers_required:
        return OrderTask.DIRECTION_SELL
    else:
        return ""