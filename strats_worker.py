# Setup Django settings and models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acacia_main.settings")

import django
django.setup()

# Begin program
import time

from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()

from main.models import Strategy
from main.strategy.evaluate import evaluate_strategy

from trades.models import OrderTask
from trades.views import fill_order_amount, calc_total_trades

from exchanges.abstract import APIError


def batch_run_strategies():
    strategies = Strategy.objects.all()

    for strategy in strategies:
        for bot in strategy.bots.filter(enabled=True):
            direction = evaluate_strategy(strategy, bot.exchange, bot.trading_pair)
            if direction == OrderTask.DIRECTION_BUY or \
                direction == OrderTask.DIRECTION_SELL:
                
                if len(bot.api_key) > 0 and len(bot.api_secret) > 0:
                    current_tasks = OrderTask.objects.filter(
                        user=bot.user,
                        exchange=bot.exchange,
                        trading_pair=bot.trading_pair
                    )
                    n = current_tasks.count()
                    if n == 0 or n > 1 or (
                        n == 1 and current_tasks[0].direction != direction
                    ):
                        current_tasks.delete()

                        new_order = OrderTask()
                        new_order.user = bot.user
                        new_order.exchange = bot.exchange
                        new_order.api_key = bot.api_key
                        new_order.api_secret = bot.api_secret
                        new_order.api_id = bot.api_id
                        new_order.trading_pair = bot.trading_pair
                        new_order.direction = direction
                        new_order.time = OrderTask.DEFAULT_EXECUTION_TIME
                        
                        order_filled = False
                        try:
                            fill_order_amount(
                                new_order,
                                p_reserve=bot.primary_reserve,
                                s_reserve=bot.secondary_reserve
                            )
                            order_filled = True
                        except APIError as e:
                            print "error:", str(e)
                        
                        if order_filled:
                            new_order.start_timestamp = int(time.time())
                            new_order.deadline_timestamp = int(time.time()) + \
                                int(OrderTask.DEFAULT_EXECUTION_TIME)

                            new_order.total_trades = calc_total_trades(new_order)
                            new_order.save()
                            #print "new order:", new_order.pk
    
    
batch_run_strategies()
# http://goo.gl/ZqzB49
scheduler = BackgroundScheduler()
scheduler.add_job(batch_run_strategies, 'interval', seconds=60)
scheduler.start()

try:
    # keeps the main thread alive
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary but should be done if possible
    scheduler.shutdown()