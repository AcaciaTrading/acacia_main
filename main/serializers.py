from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from main.models import *

import json


class AverageCrossoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AverageCrossover
        fields = (
            'first_type', 'first_interval', 'second_type',
            'second_interval', 'buy_threshold', 'sell_threshold'
        )
        
        
class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('indicator_type', 'buy_threshold', 'sell_threshold', 'strategy')
        write_only_fields = ('strategy',)
        
        
class StrategySerializer(serializers.ModelSerializer):
    #average_crossover = AverageCrossoverSerializer()
    class Meta:
        model = Strategy
        fields = (
            'id', 'name', 'time_interval', 'buy_triggers_required',
            'sell_triggers_required', 'average_crossover',
            'indicators'
        )
        read_only_fields = ('average_crossover', 'indicators',)
        depth = 1
        
        
class TradingBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingBot
        fields = (
            'strategy', 'exchange', 'trading_pair',
            'api_key', 'api_secret', 'api_id',
            'enabled', 'primary_reserve', 'secondary_reserve', 'name'
        )
        
        
class BacktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backtest
        fields = (
            'strategy', 'exchange', 'trading_pair',
            'timestamp_start', 'timestamp_end', 'profit_primary',
            'profit_secondary', 'done'
        )
        read_only_fields = ('profit', 'done',)