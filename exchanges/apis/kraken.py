from exchanges.abstract import *
from auths import KrakenAuth, get_nonce

import time
import datetime

class Kraken(Exchange):
    #key 9frTvyg/BsL2SI5Y6KxygtGhOhOKpZR7dd21DlaXw4UC6skNjlPB83+D
    #secret 3fzdyDMDYO0lKrwH4ZsexIE5BnZi9o/8hXlb6Yl1NG9a0oRAtQUGWa/ZmzhtPdxFO4SbymHNK71UA/YZjB50og==
    
    # key bad w7r+jZO98m1MVJZvcOByJiGUdvElqLxY5aXSDlCcj5BsmBvaDZhzkVZS
    # secret bad fmwx89Uk9joOuS5BwLIg8rCsLC+8XzxmyAtdaV6RyGwDIRyTlTvjRRKyEoD4O5pckhVKDpqh9p2bhdA4Fnl+eA==
    
    PUBLIC_URL = "https://api.kraken.com/0/public/"
    PRIVATE_URL = "https://api.kraken.com/0/private/"
    PAIRS = (
        "xbt_cad", "xbt_eur", "xbt_jpy", 
        "ltc_eur", "xbt_ltc", "eth_jpy", 
        "eth_gbp", "xbt_gbp", "xbt_usd", 
        "ltc_usd", "eth_cad", "eth_xbt", 
        "xbt_nmc", "eth_usd", "eth_eur", 
        "xbt_xlm", "xbt_xrp", "xbt_xdg", 
    )
    PAIR_NAMES = {u'xbt_cad': u'XXBTZCAD', u'xbt_eur': u'XXBTZEUR', 
                 u'xbt_xlm': u'XXBTXXLM', u'ltc_eur': u'XLTCZEUR', 
                 u'eth_jpy': u'XETHZJPY', u'eth_eur': u'XETHZEUR', 
                 u'xbt_xdg': u'XXBTXXDG', u'eth_gbp': u'XETHZGBP', 
                 u'xbt_ltc': u'XXBTXLTC', u'xbt_usd': u'XXBTZUSD', 
                 u'ltc_usd': u'XLTCZUSD', u'eth_cad': u'XETHZCAD', 
                 u'eth_xbt': u'XETHXXBT', u'xbt_nmc': u'XXBTXNMC', 
                 u'eth_usd': u'XETHZUSD', u'xbt_gbp': u'XXBTZGBP', 
                 u'xbt_xrp': u'XXBTXXRP', u'xbt_jpy': u'XXBTZJPY'}
    FEES = (
        {"amount":0, "fee":0.0026},
        {"amount":10000, "fee":0.0024},
        {"amount":50000, "fee":0.0022},
        {"amount":100000, "fee":0.002},
        {"amount":250000, "fee":0.0018},
        {"amount":500000, "fee":0.0016},
        {"amount":1000000, "fee":0.0014},
        {"amount":5000000, "fee":0.0012},
        {"amount":10000000, "fee":0.0010},
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
        params["nonce"] = get_nonce("Kraken_" + auth[0] + auth[1])
        
        r = requests.post(
            self.PRIVATE_URL + method,
            data=params,
            auth=KrakenAuth(auth[0], auth[1], method, params)
        )
        #print params
        #print self.PRIVATE_URL + method
        #print "\n", method
        #print r.status_code
        #print r.content
        r = r.json()
        if type(r) is dict and r.get("error"):
            raise APIError(r["error"])
        return r["result"]
    
    def pair_detail(self, pair):
        # NOT IMPLEMENTED
        if not pair in self.PAIRS:
            raise APIError("Invalid pair name: %s" % pair)
        r = self.public_json("Ticker?pair=" + PAIR_NAMES[pair])
        r = r['result']
        ticker = Ticker(
            low=float(r["l"][0]), high=float(r["h"][0]),
            average=float(r["p"][0]), bid=float(r["b"][0]),
            ask=float(r["a"][0]), last=float(r["c"][0])
        )
        volume = float(r["v"][0])
        
        r = self.public_json("Depth?pair="+PAIR_NAMES[pair])['result']
        bids = [(float(x[0]), float(x[1])) for x in r["bids"]]
        asks = [(float(x[0]), float(x[1])) for x in r["asks"]]
        orderbook = OrderBook(bids, asks)
        return Pair(ticker, volume, orderbook, self.FEES)
    
    def pair_ticker(self, pair):
        # NOT IMPLEMENTED
        if not pair in self.PAIRS:
            raise APIError("Invalid pair name: %s" % pair)
        r = self.public_json("Ticker?pair=" + PAIR_NAMES[pair])
        r = r['result']
        ticker = Ticker(
            low=float(r["l"][0]), high=float(r["h"][0]),
            average=float(r["p"][0]), bid=float(r["b"][0]),
            ask=float(r["a"][0]), last=float(r["c"][0]))
        
    def user_detail(self, auth):
        r = self.private_json("Balance", auth)
        balances = {}
        for cur, amount in r.items():
            balances[str(self.cur_convert(cur))] = float(amount)
            
        r = self.private_json("TradesHistory", auth)
        print r
        trades = []
        for t_id, trade in r["trades"].items():
            trades.append(
                Trade(
                    self.pair_convert(trade["pair"]), float(trade["price"]),
                    float(trade["vol"]), trade["type"],
                    int(trade["time"])
                )
            )
        return User(balances, trades)
    
    def api_key_detail(self, auth):
        # some methods return 'invalid params' with or without permission
        perm = APIKey.PERMISSIONS
        
        perm[APIKey.USER_BALANCES] = self.try_permission(
            "Balance",
            auth,
            errors_ok=False
        )
        perm[APIKey.USER_TRADES] = self.try_permission(
            "TradesHistory", auth
        )
        
        perm[APIKey.ORDER_LIST] = self.try_permission("OpenOrders", auth)
        perm[APIKey.ORDER_DETAIL] = self.try_permission("QueryOrders", auth)
        perm[APIKey.ORDER_CREATE] = self.try_permission("AddOrder", auth)
        perm[APIKey.ORDER_DELETE] = self.try_permission("CancelOrder", auth)
        
        return APIKey(perm)
    
    def try_permission(self, permission, auth, errors_ok=True):
        try:
            r = self.private_json(permission, auth)
        except APIError as e:
            if errors_ok and str(e) == "[u'EGeneral:Permission denied']":
                return 0
            elif not errors_ok:
                raise APIError(str(e))
        return 1
    
    def order_list(self, auth):
        # NOT IMPLEMENTED
        try:
            r = self.private_json("OpenOrders", auth)
        except APIError as e:
            if str(e) == "no orders":
                return []
            else:
                raise APIError(str(e))
        return self.orders_from_dict(r)
    
    def order_detail(self, order_id, auth):
        # NOT IMPLEMENTED
        r = self.private_json("QueryOrders", auth, params={"txid":order_id})
        return self.orders_from_dict(r)
    
    def order_create(self, order, auth):
        # NOT IMPLEMENTED
        if not order.order_type in self.ORDER_TYPES:
            raise APIError("Invalid order type.")
            
        params = {
            "pair":order.pair,
            "type":order.direction,
            "price":order.price,
            "volume":order.amount
        }
        r = self.private_json(order.direction, auth, params=params)
        return r["id"]
    
    def order_delete(self, order_id, auth):
        # NOT IMPLEMENTED
        self.private_json("cancel_order", auth, params={"txid":order_id})
    
    
    def orders_from_dict(self, data):
        # NOT IMPLEMENTED
        orders = []
        for order_id, order in data.iteritems():
            amount = order["vol"]
            amount_remaining = None
            if order.get("start_amount"):
                amount_remaining = amount
                amount = order["start_amount"]
            orders.append(Order(order['descr']["pair"], Order.LIMIT_ORDER, order['descr']["type"], amount, price=order["price"], order_id=order[refid]))
        return orders
    
    def cur_convert(self, cur):
        return cur[1:].lower()
    
    def pair_convert(self, pair):
        return self.cur_convert(pair[:4]) + "_" + self.cur_convert(pair[4:])