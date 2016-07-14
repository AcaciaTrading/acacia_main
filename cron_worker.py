# Setup Django settings and models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acacia_main.settings")

import django
django.setup()

# Begin program
import time
import threading

from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()

from prices.interface import prices_append
from exchanges.views import EXCHANGE_APIS

from billing.collect import batch_update_customers

def batch_fetch_prices():
    print "fetching prices..."
    for exchange_name, exchange in EXCHANGE_APIS.items():
        for pair in exchange.PAIRS:
            thr = threading.Thread(
                target=store_price,
                args=(exchange, exchange_name, pair,),
                kwargs={}
            )
            thr.start()
            
def store_price(exchange, exchange_name, pair):
    price = exchange.pair_ticker(pair).bid
    prices_append(exchange_name, pair, price)
            

# http://goo.gl/ZqzB49
scheduler = BackgroundScheduler()
scheduler.add_job(batch_fetch_prices, 'interval', seconds=60)
scheduler.add_job(batch_update_customers, 'interval', hours=6)
scheduler.start()

try:
    # keeps the main thread alive
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary but should be done if possible
    scheduler.shutdown()