from exchanges.abstract import *
from auths import BitstampAuth

import time
import datetime

class Bitstamp(Exchange):
    #key = "3VdU8WePKjsDQpRlvHV4dxrrzSFqsNvE"
    #secret = "WLjeD9KXmTTOHVadCOP9dThiLldkRIrd"
    #user_id = 909412
    
    PUBLIC_URL = "https://www.bitstamp.net/api/"
    PRIVATE_URL = PUBLIC_URL
    PAIRS = (
        "btc_usd",
    )
    # in USD
    FEES = (
        {"amount":0, "fee":0.0025},
        {"amount":20000, "fee":0.0024},
        {"amount":100000, "fee":0.0022},
        {"amount":200000, "fee":0.002},
        {"amount":400000, "fee":0.0015},
        {"amount":600000, "fee":0.0014},
        {"amount":1000000, "fee":0.0013},
        {"amount":2000000, "fee":0.0012},
        {"amount":4000000, "fee":0.0011},
        {"amount":20000000, "fee":0.0010},
    )
    FEES_CUR = "usd"
    ORDER_TYPES = (
        Order.LIMIT_ORDER,
    )
    MIN_ORDER = 5.0
    MIN_ORDER_CUR = "usd"
    
    
    def public_json(self, url):
        r = requests.get(self.PUBLIC_URL + url)
        r = r.json()
        if r.get("error"):
            raise APIError(r["error"])
        return r
    
    def private_json(self, method, auth, params={}):
        r = requests.post(
            self.PRIVATE_URL + method + "/",
            data=BitstampAuth().update_params(
                params, auth[0], auth[1], auth[2]
            )
        )
        r = r.json()
        if type(r) is dict and r.get("error"):
            raise APIError(r["error"])
        return r
    
    def pair_detail(self, pair):
        if not pair in self.PAIRS:
            raise APIError("Invalid pair name: %s" % pair)
        r = self.public_json("ticker/")
        ticker = Ticker(
            low=float(r["low"]), high=float(r["high"]),
            average=float(r["vwap"]), bid=float(r["bid"]),
            ask=float(r["ask"]), last=float(r["last"])
        )
        volume = float(r["volume"])
        
        r = self.public_json("order_book/")
        bids = [(float(x[0]), float(x[1])) for x in r["bids"]]
        asks = [(float(x[0]), float(x[1])) for x in r["asks"]]
        orderbook = OrderBook(bids, asks)
        return Pair(ticker, volume, orderbook, self.FEES)
    
    def pair_ticker(self, pair):
        r = self.public_json("ticker/")
        return Ticker(
            low=float(r["low"]), high=float(r["high"]),
            average=float(r["vwap"]), bid=float(r["bid"]),
            ask=float(r["ask"]), last=float(r["last"])
        )
        
    def user_detail(self, auth):
        r = self.private_json("balance", auth)
        balances = {"btc":float(r["btc_available"]), "usd":float(r["usd_available"])}
        r = self.private_json("user_transactions", auth)
        trades = []
        for trade in r:
            if float(trade["btc_usd"]) != 0.0:
                btc_amount = float(trade["btc"])
                if btc_amount < 0.0:
                    trade_type = "sell"
                else:
                    trade_type = "buy"
                timestamp = int(time.mktime(datetime.datetime.strptime(trade["datetime"], "%Y-%m-%d %H:%M:%S").timetuple()))
                trades.append(
                    Trade(
                        "btc_usd", float(trade["btc_usd"]),
                        abs(btc_amount), trade_type,
                        timestamp
                    )
                )
        return User(balances, trades)
    
    def api_key_detail(self, auth):
        perm = APIKey.PERMISSIONS
        
        perm[APIKey.USER_BALANCES] = self.try_permission("balance", auth, errors_ok=False)
        perm[APIKey.USER_TRADES] = self.try_permission(
            "user_transactions", auth
        )
        
        perm[APIKey.ORDER_LIST] = self.try_permission("open_orders", auth)
        perm[APIKey.ORDER_DETAIL] = self.try_permission("order_status", auth)
        perm[APIKey.ORDER_CREATE] = self.try_permission("buy", auth)
        perm[APIKey.ORDER_DELETE] = self.try_permission("cancel_order", auth)
        
        return APIKey(perm)
    
    def try_permission(self, permission, auth, errors_ok=True):
        try:
            r = self.private_json(permission, auth)
        except APIError as e:
            if errors_ok and str(e) == "No permission found":
                return 0
            elif not errors_ok:
                raise APIError(str(e))
        return 1
    
    def order_list(self, auth):
        r = self.private_json("open_orders", auth)
        return self.orders_from_list(r)
    
    def order_detail(self, order_id, auth):
        orders = self.private_json("open_orders", auth)
        order = self.private_json("order_status", auth, params={"id":order_id})
        
        result = self.orders_from_list(orders, order_id=int(order_id), trades=order["transactions"])
        if len(result) > 0:
            return result
        else:
            raise APIError("Order not found.")
    
    def order_create(self, order, auth):
        if not order.order_type in self.ORDER_TYPES:
            raise APIError("Invalid order type.")
            
        params = {
            "price":order.price,
            "amount":order.amount
        }
        r = self.private_json(order.direction, auth, params=params)
        return r["id"]
    
    def order_delete(self, order_id, auth):
        self.private_json("cancel_order", auth, params={"id":order_id})
    
    
    def orders_from_list(self, data, order_id=None, trades=None):
        orders = []
        for order in data:
            if order_id == None or order_id == order["id"]:
                amount = order["amount"]
                amount_remaining = None
                if trades != None:
                    amount_remaining = float(amount)
                    for trade in trades:
                        amount_remaining -= float(trade["btc"])
                    amount_remaining = float(amount_remaining)
                if order["type"] == 1:
                    order_type = "sell"
                else:
                    order_type = "buy"
                orders.append(
                    Order(
                        "btc_usd",
                        Order.LIMIT_ORDER,
                        order_type,
                        float(amount),
                        price=float(order["price"]),
                        order_id=int(order["id"]),
                        amount_remaining=amount_remaining
                    )
                )
        return orders