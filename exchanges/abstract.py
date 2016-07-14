from abc import ABCMeta, abstractmethod
import requests

class Exchange(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def pair_detail(self, pair): pass
    
    # pair_ticker is not an API method - it's only used for the prices API
    @abstractmethod
    def pair_ticker(self, pair): pass
    
    @abstractmethod
    def user_detail(self, auth): pass
    
    @abstractmethod
    def api_key_detail(self, auth): pass
    
    @abstractmethod
    def order_list(self, auth): pass
    @abstractmethod
    def order_detail(self, order_id, auth): pass
    @abstractmethod
    def order_create(self, order, auth): pass
    @abstractmethod
    def order_delete(self, order_id, auth): pass
    
    
class Pair(object):
    def __init__(self, ticker, volume, orderbook, fees):
        self.ticker = ticker
        self.volume = volume
        self.depth = orderbook
        # list of {"amount":amount, "fee":fee}
        self.fees = fees
        
    def data(self):
        return {
            "ticker":self.ticker.data(),
            "volume":self.volume,
            "depth":self.depth.data(),
            "fees":self.fees
        }
        
        
class Ticker(object):
    def __init__(self, low=None, high=None, average=None, bid=None, ask=None, last=None):
        self.low = low
        self.high = high
        self.average = average
        self.bid = bid
        self.ask = ask
        self.last = last
        
    def data(self):
        return {
            "low":self.low,
            "high":self.high,
            "average":self.average,
            "bid":self.bid,
            "ask":self.ask,
            "last":self.last
        }
        
        
class OrderBook(object):
    # Bids / asks format: [(price, amount), ...]
    def __init__(self, bids, asks):
        self.bids = bids
        self.asks = asks
        
    def data(self):
        return {"bids":self.bids, "asks":self.asks}
    
    
class User(object):
    def __init__(self, balances, trades):
        self.balances = balances
        self.trades = trades
        
    def data(self):
        trades = []
        for trade in self.trades:
            trades.append(trade.data())
        return {"balances":self.balances, "trades":trades}
    
    
class APIKey(object):
    USER_BALANCES = "user_balances"
    USER_TRADES = "user_trades"
    
    ORDER_LIST = "order_list"
    ORDER_DETAIL = "order_detail"
    ORDER_CREATE = "order_create"
    ORDER_DELETE = "order_delete"
    
    PERMISSIONS = {
        USER_BALANCES:0 ,USER_TRADES:0 ,
        ORDER_LIST:0 , ORDER_DETAIL:0 , ORDER_CREATE:0 , ORDER_DELETE:0
    }
    
    def __init__(self, permissions):
        self.permissions = permissions
        
    def data(self):
        return {"permissions": self.permissions}
    
    
class Order(object):
    LIMIT_ORDER = "limit"
    MARKET_ORDER = "market"
    STOP_LOSS_ORDER = "stop-loss"
    TAKE_PROFIT_ORDER = "take-profit"
    STOP_LOSS_PROFIT_ORDER = "stop-loss-profit"
    STOP_LOSS_PROFIT_LIMIT_ORDER = "stop-loss-profit-limit"
    STOP_LOSS_LIMIT_ORDER = "stop-loss-limit"
    TAKE_PROFIT_LIMIT_ORDER = "take-profit-limit"
    TRAILING_STOP_ORDER = "trailing-stop"
    TRAILING_STOP_LIMIT_ORDER = "trailing-stop-limit"
    STOP_LOSS_AND_LIMIT_ORDER = "stop-loss-and-limit"
    
    def __init__(
        self, pair, order_type,
        direction, amount, price=None,
        price2=None, order_id=None, amount_remaining=None):
        """Initializes Order object.  Note: order_type should be a valid order
        type.
        """
        self.pair = pair
        self.order_type = order_type
        # Direction is buy or sell
        self.direction = direction
        self.amount = amount
        
        self.price = price
        self.price2 = price2
        self.order_id = order_id
        self.amount_remaining = amount_remaining
        
    def data(self):
        result = {
            "pair":self.pair,
            "order_type":self.order_type,
            "direction":self.direction,
            "amount":self.amount
        }
        if self.price != None:
            result["price"] = self.price
        if self.price2 != None:
            result["price2"] = self.price2
        if self.order_id != None:
            result["order_id"] = self.order_id
        if self.amount_remaining != None:
            result["amount_remaining"] = self.amount_remaining
        return result
            
            
class Trade(object):
    def __init__(self, pair, price, amount, order_type, timestamp):
        self.pair = pair
        self.price = price
        self.amount = amount
        self.order_type = order_type
        self.timestamp = timestamp
        
    def data(self):
        return {
            "pair": self.pair,
            "price": self.price,
            "amount": self.amount,
            "order_type": self.order_type,
            "timestamp": self.timestamp
        }
        
        
class APIError(Exception):
    pass