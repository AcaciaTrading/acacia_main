from django.db import models

from django.contrib.auth.models import User

from main.strategy.indicators import AVERAGE_METHODS, INDICATOR_METHODS

# Create your models here.
class Strategy(models.Model):
    TIME_INTERVAL_OPTIONS = (
        (60, "1 Minute"),
        (300, "5 Minutes"),
        (900, "15 Minutes"),
        (1800, "30 Minutes"),
        (3600, "One Hour"),
    )
    
    TYPE_SIMPLE_RULE = 0
    TYPE_COMPLEX_RULE = 1
    TYPE_SCRIPT = 2
    
    EDIT_URL = "strategy_page"
    OBJ_NAME = "strategy"
    NO_PROFIT_MESSAGE = "No Backtests"
    PROFIT_MESSAGE = "Last Backtest"
    
    STRATEGY_TYPES = (
        (TYPE_SIMPLE_RULE, "Simple rule-based"),
        (TYPE_COMPLEX_RULE, "Complex rule-based"),
        (TYPE_SCRIPT, "Script-based"),
    )
    
    user = models.ForeignKey(User, related_name="strategies")
    name = models.CharField(max_length=100, default="Untitled Strategy")
    
    time_interval = models.IntegerField(choices=TIME_INTERVAL_OPTIONS, default=3600)
    
    buy_triggers_required = models.IntegerField(default=1)
    sell_triggers_required = models.IntegerField(default=1)
    
    average_crossover = models.OneToOneField('AverageCrossover', related_name="strategy", null=True, blank=True)
    
    def has_profit(self):
        return self.last_backtest() != None
    
    def profit(self):
        backtest = self.last_backtest()
        return (backtest.profit_primary, backtest.profit_secondary,)
    
    def last_backtest(self):
        result = self.backtests.filter(done=True).order_by('-pk')
        if result.count() == 0:
            return None
        else:
            return result[0]
        
    def indicators_list(self):
        return [x.indicator_type for x in self.indicators.all()]
    
    
class AverageCrossover(models.Model):
    AVERAGE_OPTIONS = [(x[0], x[0],) for x in AVERAGE_METHODS.items()]
    INTERVAL_OPTIONS = [(x, x,) for x in range(1, 41)]
    
    first_type = models.CharField(max_length=3, choices=AVERAGE_OPTIONS, default="EMA")
    first_interval = models.IntegerField(default=10, choices=INTERVAL_OPTIONS)
    
    second_type = models.CharField(max_length=3, choices=AVERAGE_OPTIONS, default="EMA")
    second_interval = models.IntegerField(default=21, choices=INTERVAL_OPTIONS)
    
    buy_threshold = models.FloatField(default=0.25)
    sell_threshold = models.FloatField(default=0.25)
    
    
class Indicator(models.Model):
    INDICATOR_OPTIONS = [(x[0], x[0],) for x in INDICATOR_METHODS.items()]
    
    strategy = models.ForeignKey(Strategy, related_name="indicators")
    
    indicator_type = models.CharField(max_length=25, choices=INDICATOR_OPTIONS)
    buy_threshold = models.FloatField()
    sell_threshold = models.FloatField()
    

class TradingBot(models.Model):
    EDIT_URL = "bot_page"
    OBJ_NAME = "bot"
    NO_PROFIT_MESSAGE = "No Recent Trades"
    PROFIT_MESSAGE = "30-day Profit"
    
    user = models.ForeignKey(User, related_name="bots")
    strategy = models.ForeignKey(Strategy, related_name="bots")
    name = models.CharField(max_length=100, default="Untitled Bot")
    
    enabled = models.BooleanField(default=False)
    
    exchange = models.CharField(max_length=20, default="btc-e")
    trading_pair = models.CharField(max_length=20, default="btc_usd")
    
    api_key = models.CharField(max_length=150, blank=True)
    api_secret = models.CharField(max_length=150, blank=True)
    api_id = models.CharField(max_length=20, blank=True)
    
    primary_reserve = models.FloatField(default=0)
    secondary_reserve = models.FloatField(default=0)
    

class BotTrade(models.Model):
    bot = models.ForeignKey(TradingBot, related_name="trades")
    
    exchange = models.CharField(max_length=20)
    trading_pair = models.CharField(max_length=20)
    direction = models.CharField(max_length=4)
    amount = models.FloatField()
    timestamp = models.IntegerField()
    

class Backtest(models.Model):
    strategy = models.ForeignKey(Strategy, related_name="backtests")
    
    exchange = models.CharField(max_length=20)
    trading_pair = models.CharField(max_length=20)
    
    timestamp_start = models.IntegerField()
    timestamp_end = models.IntegerField()
    
    profit_primary = models.FloatField(default=0.0)
    profit_secondary = models.FloatField(default=0.0)
    done = models.BooleanField(default=False)