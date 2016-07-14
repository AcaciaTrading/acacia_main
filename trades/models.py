from django.db import models

from django.contrib.auth.models import User

import time

# Create your models here.
class OrderTask(models.Model):
    MIN_ORDER_AMOUNT = 0.03
    MIN_ORDER_INTERVAL = 15
    
    DIRECTION_BUY = "buy"
    DIRECTION_SELL = "sell"
    
    REQUIRED_FIELDS = [
        "exchange", "api_key", "api_secret", "trading_pair",
        "direction", "time"
    ]
    
    DEFAULT_EXECUTION_TIME = 1800
    
    user = models.ForeignKey(User, related_name="order_tasks")
    
    exchange = models.CharField(max_length=15)
    api_key = models.CharField(max_length=250)
    api_secret = models.CharField(max_length=250)
    api_id = models.CharField(max_length=50, blank=True)
    
    trading_pair = models.CharField(max_length=10)
    direction = models.CharField(max_length=4)
    
    amount = models.FloatField(default=-1)
    amount_remaining = models.FloatField(default=-1)
    autofilled = models.BooleanField(default=False)
    
    start_timestamp = models.IntegerField(default=-1)
    deadline_timestamp = models.IntegerField(default=-1)
    
    trades_made = models.IntegerField(default=0)
    total_trades = models.IntegerField(default=-1)
    
    def json_fields(self):
        return {
            "id":self.pk,
            "exchange":self.exchange,
            "trading_pair":self.trading_pair,
            "direction":self.direction,
            "amount":self.amount,
            "amount_remaining":self.amount_remaining,
            "time_remaining":max(0, int(self.deadline_timestamp - time.time()))
        }