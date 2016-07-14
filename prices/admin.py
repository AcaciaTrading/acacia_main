from django.contrib import admin

from main.models import *

# Register your models here.
admin.site.register(Strategy)
admin.site.register(AverageCrossover)
admin.site.register(Indicator)
admin.site.register(TradingBot)
admin.site.register(BotTrade)
admin.site.register(Backtest)