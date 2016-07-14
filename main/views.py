from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, user_passes_test
from billing.utils import billing_check, BillingCheckMixin
from billing.models import Plan

from rest_framework.authtoken.models import Token

from utils.views import *

from main.serializers import *
from main.models import Indicator, Strategy, Backtest, TradingBot
from main.strategy.indicators import INDICATORS, INDICATOR_EXPLANATIONS
from main.strategy.backtest import run_backtest
from exchanges.views import EXCHANGE_APIS
from prices.interface import prices_get

import json
import time
import datetime


# Create your views here.
def landing(request):
    if request.user.is_authenticated():
        return redirect("main:index")
    else:
        return render(request, "landing/index.html")

@login_required
@user_passes_test(billing_check)
def index(request):
    create_token_if_not_exists(request.user)
    
    bots = request.user.bots.all()
    strats = request.user.strategies.all()
    
    if bots.count() == 0 and strats.count() == 0:
        new_bot(request.user, "Default")
        bots = request.user.bots.all()
        strats = request.user.strategies.all()
    
    return render(request, "main/index.html", {
        "bots": bots,
        "strats": strats
    })
    
@login_required
def strategy_page(request, id):
    strats = request.user.strategies.filter(pk=id)
    if strats.count() == 1:
        return render(
            request,
            "main/strategy.html",
            item_context(strats[0], StrategySerializer)
        )
    
@login_required
def bot_page(request, id):
    bots = request.user.bots.filter(pk=id)
    if bots.count() == 1:
        return render(
            request,
            "main/bot.html",
            item_context(bots[0], TradingBotSerializer)
        )
    
class PlanList(ListView):
    model = Plan
    template_name = "landing/pricing.html"
    
    def get_queryset(self):
        return Plan.objects.all().order_by("price_cents")
    
    
def item_context(item, serializer):
    return {
        "item":item,
        "exchange_list" : EXCHANGE_APIS,
        "Strategy":Strategy,
        "AverageCrossover":AverageCrossover,
        "indicators":INDICATORS,
        "indicator_explanations":[
            (x, INDICATOR_EXPLANATIONS[x],) for x in INDICATORS
        ]
    }

def graph_data(request):
    prices = prices_get(
        request.GET.get("exchange", "btc-e"),
        request.GET.get("pair", "btc_usd"),
        num_prices=4320
    )
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="menlohacks-export.csv"'
    writer = UnicodeWriter(response)
    writer.writerow(["Date", "Open", "High", "Low", "Close"])
    
    p_open = prices[0]
    p_high = prices[0]
    p_low = prices[0]
    current_time = time.time()
    
    for index in range(0, len(prices)):
        p_cur = prices[index]
        if index % 30 == 0:
            date = datetime.datetime.fromtimestamp(current_time - 60 * index).strftime('%-d-%b-%y %H:%M')
            p_close = prices[index - 1]
            writer.writerow(
                [date, p_close, p_high, p_low, p_open]
            )
            p_open = p_cur
            p_high = p_cur
            p_low = p_cur
        else:
            p_high = p_cur if p_cur > p_high else p_high
            p_low = p_cur if p_cur < p_low else p_low
    return response

# Strategy API below
class StrategyList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        strategies = request.user.strategies.all()
        result = [StrategySerializer(x).data for x in strategies]
        return r_success(result)


class StrategyDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        strategies = request.user.strategies.filter(pk=request.GET.get("id"))

        if strategies.count() == 1:
            return r_success(StrategySerializer(strategies[0]).data)
        else:
            return r_failure("Strategy not found.")

    def post(self, request):
        strategies = request.user.strategies.filter(pk=request.POST.get("id"))
        if strategies.count() == 1:
            strategy = strategies[0]
            params = request.POST.copy()
            #print params
            try:
                if params["average_crossover"] in ("null", ""):
                    try:
                        strategy.average_crossover.delete()
                    except Exception:
                        pass
                    
                else:
                    try:
                        serializer = AverageCrossoverSerializer(
                            strategy.average_crossover,
                            data=json.loads(params["average_crossover"]),
                            partial=True
                        )
                    except Exception:
                        serializer = AverageCrossoverSerializer(
                            data=json.loads(params["average_crossover"])
                        )

                    if serializer.is_valid():
                        obj = serializer.save()
                        strategy.average_crossover = obj
                        strategy.save()
                    else:
                        return r_failure(serializer.errors)
            except KeyError:
                pass
            
            
            try:
                indicators = json.loads(params["indicators"])
                strategy.indicators.all().delete()
                for indicator in indicators:
                    indicator["strategy"] = strategy.pk
                    serializer = IndicatorSerializer(data=indicator)
                    if serializer.is_valid():
                        obj = serializer.save()
                    else:
                        return r_failure(serializer.errors)
            except Exception as e:
                print str(e)
                    
            
            serializer = StrategySerializer(
                strategy,
                data=params,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                
                return r_success("Strategy updated successfully")
            else:
                return r_failure(serializer.errors)
        else:
            return r_failure("Strategy not found.")
        
        
class StrategyDelete(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        print "hello!"
        strats = request.user.strategies.filter(pk=request.POST.get("id"))
        if strats.count() == 1:
            strat = strats[0]
            if strat.pk in [x.strategy.pk for x in request.user.bots.all()]:
                return r_failure(
                    "Deletion failed - you have bots using this strategy."
                )
            else:
                strat.delete()
                return r_success("Strategy deleted successfully.")
        else:
            return r_failure("Strategy not found.")


class StrategyNew(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.POST.get("name") and request.POST.get("type"):
            strategy_types = [x[0] for x in Strategy.STRATEGY_TYPES]
            if int(request.POST["type"]) in strategy_types:
                strategy = new_strategy(
                    request.user,
                    request.POST["name"],
                    int(request.POST["type"])
                )
                return r_success(strategy.pk)
            else:
                return r_failure(
                    "'type' parameter must be one of: %s" % strategy_types
                )
        else:
            return r_failure("Must supply 'name' and 'type' parameters.")


class BotList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bots = request.user.bots.all()
        result = [TradingBotSerializer(x).data for x in bots]
        return r_success(result)


class BotDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bots = request.user.bots.filter(pk=request.GET.get("id"))

        if bots.count() == 1:
            return r_success(TradingBotSerializer(bots[0]).data)
        else:
            return r_failure("Bot not found.")

    def post(self, request):
        bots = request.user.bots.filter(pk=request.POST.get("id"))
        if bots.count() == 1:
            bot = bots[0]
            print request.POST
            serializer = TradingBotSerializer(bot, data=request.POST, partial=True)
            if serializer.is_valid():
                serializer.save()
                return r_success("Bot updated successfully")
            else:
                return r_failure(serializer.errors)
        else:
            return r_failure("Bot not found.")
        
        
class BotDelete(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        bots = request.user.bots.filter(pk=request.POST.get("id"))
        if bots.count() == 1:
            bots[0].delete()
            return r_success("Bot deleted successfully.")
        else:
            return r_failure("Bot not found.")


class BotNew(BillingCheckMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.POST.get("name"):
            if request.user.customer.can_add_more_bots() == True:
                return r_success(
                    new_bot(request.user, request.POST["name"])
                )
            else:
                return r_failure(
                    "You cannot add any more bots with your current plan."
                )
        else:
            return r_failure("Must supply 'name' parameter.")
        
        
class BacktestDetail(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        backtest = Backtest.objects.filter(pk=request.GET.get("id"))

        if backtest.count() == 1:
            return r_success(BacktestSerializer(backtest[0]).data)
        else:
            return r_failure("Backtest not found.")
    
    def post(self, request):
        params = {key:val[0] for key, val in dict(request.POST.copy()).items()}
        print params
        trim = False
        if params.get("timestamp_start") == None:
            params["timestamp_start"] = int(time.time() - 2592000)
            trim = True
        if params.get("timestamp_end") == None:
            params["timestamp_end"] = int(time.time())
            
        print params
        serializer = BacktestSerializer(data=params)
        if serializer.is_valid():
            backtest = serializer.save()
            try:
                trades = run_backtest(backtest, trim=trim)
                result = BacktestSerializer(backtest).data
                result["trades"] = trades
                return r_success(result)
            except Exception as e:
                return r_failure(str(e))
        else:
            return r_failure(serializer.errors)
        
        
def new_bot(user, name):
    bot = TradingBot()
    bot.user = user
    bot.name = name
    strategies = user.strategies.all()
    if strategies.count() == 0:
        bot.strategy = new_strategy(
            user,
            "%s Strategy" % name,
            Strategy.TYPE_SIMPLE_RULE
        )
    else:
        bot.strategy = strategies[0]
    bot.save()
    return bot.pk
        
def new_strategy(user, name, strategy_type):
    s = Strategy()
    s.user = user
    s.name = name
    s.save()

    if strategy_type == Strategy.TYPE_SIMPLE_RULE:
        c = AverageCrossover()
        
        # defaults
        c.first_type = "EMA"
        c.first_interval = 10
        c.second_type = "EMA"
        c.second_interval = 21
        c.buy_threshold = 0.25
        c.sell_threshold = 0.25
        
        c.save()
        s.average_crossover = c
        s.save()
    return s

def create_token_if_not_exists(user) :
    try:
        x = user.auth_token.key
    except Exception:
        token = Token.objects.create(user=user)
        token.save()
        
        
import csv, codecs, cStringIO
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([str(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)