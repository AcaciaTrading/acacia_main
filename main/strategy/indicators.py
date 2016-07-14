import math

# Calculation methods for moving averages

def ema(prices, interval):
    percentage = 2 / (interval + 1)
    starting_prices = prices[interval:]
    old_average = sma(starting_prices, len(starting_prices))
                      
    for i in range(interval, 0, -1):
        old_average = (prices[i] * percentage) + (old_average * (1 - percentage))
    return old_average

def sma(prices, interval):
    p = prices[:interval]
    return sum(p) / len(p)

def tma(prices, interval):
    weights = []
    max_weight = int(round(1.0 * interval / 2))
    
    if interval % 2 == 0:
        weights += range(1, max_weight + 1)
        weights += range(max_weight, 0, -1)
    else:
        weights += range(1, max_weight + 1)
        weights += range(max_weight - 1, 0, -1)
        
    #This takes a weighted average starting from each price in the final period
    averages = [
        average_with_weights(prices[i:i + len(weights)], weights)
        for i in range(0, interval)
    ]
        
    return sma(averages, len(averages))

def dema(prices, interval):
    tmp_interval = interval+(len(prices)-interval)/2
    mult = 2.0/(tmp_interval+1)
    prev_ema = sma(prices[tmp_interval:],len(prices[tmp_interval:]))
    first_ema = []
    for i in range(tmp_interval,0,-1):
        first_ema += [prices[i]*mult + prev_ema*(1-mult)]

    return 2*ema(prices,interval) - ema(first_ema,interval)

def tema(prices, interval):
    tmp_interval = interval+(len(prices)-interval)/3
    mult = 2/(tmp_interval+1)
    prev_ema = sma(prices[tmp_interval:],len(prices[tmp_interval:]))
    first_ema = []
    for i in range(tmp_interval,0,-1):
        first_ema += [prices[i]*mult + prev_ema*(1-mult)]

    tmp_interval = (interval+tmp_interval)/2
    prev_ema = sma(first_ema[tmp_interval:],tmp_interval)
    second_ema = []
    for i in range(tmp_interval,0,-1):
        second_ema += [first_ema[i]*mult + prev_ema*(1-mult)]

    return 3*ema(prices,interval) - ema(second_ema,interval)

def average_with_weights(prices, weights):    
    length = len(weights)
    if len(prices) < length:
        length = len(prices)
        
    total = sum([prices[i] * weights[i] for i in range(0, length)])
        
    total_weight = sum(weights[0:length])
    return total / total_weight

def wma(prices, interval):
    weighted_prices = []
    weights = range(1, interval)
    
    weighted_prices = [prices[interval - i] * i for i in range(1, interval)]
        
    total_prices = sum(weighted_prices)
    total_weights = sum(weights)
    
    return total_prices / total_weights


AVERAGE_METHODS = {
    "EMA":ema,
    "SMA":sma,
    "TMA":tma,
    "WMA":wma,
    "DEMA":dema,
    "TEMA":tema
}


# Calculation methods for indicators

def macd(prices):
    macd_vals = []
    
    for i in range(0,20):
        prices_short = prices[i:]
        macd_vals.append(ema(prices_short, 12) - ema(prices_short, 24))
        
    signal_line = ema(macd_vals, 9)
    macd_line = ema(prices, 12) - ema(prices, 24)

    return round_figures((macd_line - signal_line), 5)

def rsi(prices):
    gains = filter_price_changes(prices, 'gain')
    losses = filter_price_changes(prices, 'loss')
    #print gains
    #print losses
    average_gain = rsi_average(gains)
    average_loss = rsi_average(losses)

    rsi_val = 100 - (100 / (1 + (average_gain / average_loss)))
    return round(rsi_val,2)


def rsi_average(changes):
    interval = 14
    starting = changes[:interval]
    previous = sma(starting, len(starting))
    
    #print len(changes) - interval
    
    for i in range(len(changes) - interval, 0, -1):
        #print i
        new_val = previous * (interval - 1) + changes[i] / interval
        previous = new_val
        
    return new_val

def filter_price_changes(prices, kind):
    changes = []
    old = prices[0]
    for p in prices[1:]:
        dif = p-old
        if dif > 0 and kind == 'gain':
            changes.append(abs(dif))
        elif dif < 0 and kind == 'loss':
            changes.append(abs(dif))
        else:
            changes.append(0)
        old=p
    return changes

def roc(prices):
    roc_val = ((prices[0] - prices[11]) / prices[11]) * 100
    return round_figures(roc_val, 6)

def stochastic(prices):
    interval = 14
    max_value = max(prices[:interval])
    max_index = prices[:interval].index(max_value)

    min_value = min(prices[:interval])
    min_index = prices[:interval].index(min_value)

    current_price = prices[0]

    stoch_val = 100.0 * (current_price - min_value) / (max_value - min_value)

    return stoch_val

def aroon_up(prices):
    interval = 25
    
    max_value = max(prices[:interval])
    max_index = prices[:interval].index(max_value)

    aroon_up_val = 100.0 * (interval - max_index)/interval

    return aroon_up_val

def aroon_down(prices):
    interval = 25

    min_value = min(prices[:interval])
    min_index = prices[:interval].index(min_value)

    aroon_up_val = 100.0 * (interval - min_index)/interval

    return aroon_up_val


def stoch_rsi(prices):
    gains = filter_price_changes(prices, 'gain')
    losses = filter_price_changes(prices, 'loss')

    current_average_gain = stoch_rsi_average(gains, 0)
    current_average_loss = stoch_rsi_average(losses, 0)

    current_rsi_val = 100 - (100 / (1 + (current_average_gain / current_average_loss)))

    past_rsi_list = []

    for interval_mod in range(1, 14):
        average_gain = stoch_rsi_average(gains, interval_mod)
        average_loss = stoch_rsi_average(losses, interval_mod)

        rsi_val = 100 - (100 / (1 + (average_gain / average_loss)))
        past_rsi_list.append(rsi_val)

    max_rsi = max(past_rsi_list)
    min_rsi = min(past_rsi_list)

    stoch_rsi = (current_rsi_val - min_rsi) / (max_rsi - min_rsi)
    return stoch_rsi

def stoch_rsi_average(changes, interval_mod):
    interval = 14 + interval_mod
    starting = changes[interval_mod:interval]
    previous = sma(starting)

    #print len(changes) - interval

    for i in range(len(changes) - interval, interval_mod, -1):
        #print i
        new_val = previous * (interval - 1) + changes[i] / interval
        previous = new_val

    return new_val

def ulcer_index(prices):

    percent_drawdown_squared_lst = []

    for interval_mod in range(0, 14):
        current_price = prices[interval_mod]

        price_time_period = prices[interval_mod:14 + interval_mod]
        max_time_period = max(price_time_period)

        percent_drawdown = ((current_price - max_time_period)/max_time_period) * 100
        percent_drawdown_squared_lst.append(percent_drawdown ** 2)

    squared_average = sum(percent_drawdown_squared_lst)/14
    ulcer_index = math.sqrt(squared_average)

    return ulcer_index

    
def round_figures(x, n):
    """Returns x rounded to n significant figures.
    from https://mail.python.org/pipermail/tutor/2009-September/071393.html
    """
    if x == 0:
        return x
    return round(x, int(n - math.ceil(math.log10(abs(x)))))


INDICATORS = ("MACD", "RSI", "ROC", "Stochastic", "Aroon Up", "Aroon Down")

INDICATOR_METHODS = {
    "MACD":macd,
    "RSI":rsi,
    "ROC":roc,
    "Stochastic":stochastic,
    "Aroon Up":aroon_up,
    "Aroon Down":aroon_down,
    "Stoch RSI":stoch_rsi,
    "Ulcer Index":ulcer_index
}

INDICATOR_EXPLANATIONS = {
    "MACD": (
        "The MACD is calculated by subtracting the 26-interval exponential moving average (EMA) from the 12-interval EMA. A 9-interval EMA of the MACD, called the signal line, is then plotted on top of the MACD, functioning as a trigger for buy and sell signals.",
        "This is the minimum amount that the 9 interval EMA of the MACD line needs to be above the MACD line in order for the bot to buy. Numbers from 0 to 3 generally work well, but it is possible to enter any number.",
        "This is the minimum amount that the 9 interval EMA of the MACD line needs to be below the MACD line in order for the bot to sell. Numbers from 0 to 3 generally work well, but it is possible to enter any number.",
    ),
    
    "RSI": (
        "RSI oscillates between 0 and 100. RSI can be used to identify a general trend. An RSI of above 70 generally indicates that something is overbought, and an RSI of below 30 indicates that something has been oversold.",
        "This is the value that the RSI needs to below for the bot to buy. As 50 means that it is neither growing nor decreasing, values of 40 to 50 generally work well; however, it is possible to go as low as 0 (not recommended).",
        "This is the value that the RSI needs to above for the bot to sell. As 50 means that it is neither growing nor decreasing, values of 50 to 60 generally work well; however, it is possible to go as high as 100 (not recommended).",
    ),
    
    "ROC": (
        "The rate of change is essentially the percent difference in Bitcoin throughout a time span of 12 intervals.",
        "This is the percent which Bitcoin needs to rise in 12 intervals for the bot to purchase. Values from 2 to 10 generally work well, but it is theoretically possible to enter any value.",
        "This is the percent which Bitcoin needs to fall in 12 intervals for the bot to sell. Values from -2 to -10 generally work well, but it is theoretically possible to enter any value.",
    ),
    
    "Stochastic": (
        "The Stochastic oscillator is a technical momentum indicator that compares a security's closing price to its price range over a given time period. It ranges from 0 to 100.",
        "We recommend values around 20 for the buy threshold.",
        "We recommend values around 80 for the sell threshold.",
    ),
    
    "Aroon Up":(
        "The Aroon indicators measure the number of periods since price recorded an x-day high or low. A 25-interval Aroon-Up measures the number of intervals since a 25-interval high. It ranges from 0 to 100.",
        "We recommend a low value (~20) for the buy threshold.",
        "We recommend a high value (~80) for the sell threshold.",
    ),
    
    "Aroon Down":(
        "The Aroon indicators measure the number of periods since price recorded an x-day high or low.  25-interval Aroon-Down measures the number of intervals since a 25-interval low. It ranges from 0 to 100.",
        "We recommend a high value (~80) for the buy threshold.",
        "We recommend a low value (~20) for the sell threshold.",
    )
}