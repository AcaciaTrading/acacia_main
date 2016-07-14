# Setup Django settings and models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acacia_main.settings")

import django
django.setup()

# Begin program
import time

from trades.models import OrderTask
from trades.execute import batch_execute

def trades_needed(order):
    done_proportion = 1.0 * (time.time() - order.start_timestamp) / (order.deadline_timestamp - order.start_timestamp)
    #print "%s vs. %s" % ((done_proportion * order.total_trades), order.trades_made)
    return (done_proportion * order.total_trades) >= order.trades_made
    


while True:
    OrderTask.objects.filter(
        deadline_timestamp__lt=(time.time() - 300)
    ).delete()
    
    pending_orders = OrderTask.objects.filter(
        amount_remaining__gt=0.0,
        deadline_timestamp__gt=time.time()
    )
    if pending_orders.count() > 0:
        orders = [x for x in pending_orders if trades_needed(x)]
        batch_execute(orders)
    
    time.sleep(5)