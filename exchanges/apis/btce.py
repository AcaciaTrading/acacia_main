from exchanges.abstract import *
from auths import BTCeAuth, get_nonce

class BTCe(Exchange):
    PUBLIC_URL = "https://btc-e.com/api/3/"
    PRIVATE_URL = "https://btc-e.com/tapi"
    PAIRS = (
        "btc_usd", "btc_rur", "btc_eur", "ltc_btc",
        "ltc_rur", "ltc_eur", "nmc_btc", "nmc_usd",
        "nvc_btc", "nvc_usd", "usd_rur", "eur_usd",
        "eur_rur", "ppc_btc", "ppc_usd",
    )
    FEES = (
        {"amount":0, "fee":0.001},
    )
    FEES_CUR = "btc"
    ORDER_TYPES = (
        Order.LIMIT_ORDER,
    )
    MIN_ORDER = 0.02
    MIN_ORDER_CUR = "btc"
    
    
    def public_json(self, url):
        r = requests.get(self.PUBLIC_URL + url)
        r = r.json()
        if r.get("error"):
            raise APIError(r["error"])
        return r
    
    def private_json(self, method, auth, params={}):
        params["method"] = method
        params["nonce"] = get_nonce("BTCe_" + auth[0] + auth[1])
        r = requests.post(self.PRIVATE_URL, data=params, auth=BTCeAuth(auth[0], auth[1], params))
        r = r.json()
        if r["success"] == 0:
            raise APIError(r["error"])
        return r["return"]
    
    def pair_detail(self, pair):
        if not pair in self.PAIRS:
            raise APIError("Invalid pair name: %s" % pair)
            
        r = self.public_json("ticker/" + pair)
        r = r[pair]
        ticker = Ticker(
            low=r["low"], high=r["high"], average=r["avg"],
            bid=r["sell"], ask=r["buy"], last=r["last"]
        )
        volume = r["vol_cur"]
        
        r = self.public_json("depth/" + pair)
        r = r[pair]
        orderbook = OrderBook(r["bids"], r["asks"])
        return Pair(ticker, volume, orderbook, self.FEES)
    
    def pair_ticker(self, pair):
        r = self.public_json("ticker/" + pair)
        r = r[pair]
        return Ticker(
            low=r["low"], high=r["high"], average=r["avg"],
            bid=r["sell"], ask=r["buy"], last=r["last"]
        )
        
    def user_detail(self, auth):
        r = self.private_json("getInfo", auth)
        balances = r["funds"]
        for currency, amount in balances.items():
            balances[currency] = float(amount)
            
        r = self.private_json("TradeHistory", auth)
        trades = []
        for trade_id, trade in r.iteritems():
            trades.append(
                Trade(
                    trade["pair"], trade["rate"],
                    float(trade["amount"]), trade["type"],
                    int(trade["timestamp"])
                )
            )
        return User(balances, trades)
    
    def api_key_detail(self, auth):
        try:
            r = self.private_json("getInfo", auth)
            r = r["rights"]
        except APIError as e:
            if str(e) == "api key dont have info permission":
                r = {"info":0, "trade":0}
            else:
                raise APIError(str(e))
        perm = APIKey.PERMISSIONS
        perm[APIKey.USER_BALANCES] = perm[APIKey.USER_TRADES] = \
            perm[APIKey.ORDER_LIST] = perm[APIKey.ORDER_DETAIL] = r["info"]
        
        perm[APIKey.ORDER_CREATE] = perm[APIKey.ORDER_DELETE] = r["trade"]
        
        return APIKey(perm)
    
    def order_list(self, auth):
        try:
            r = self.private_json("ActiveOrders", auth)
        except APIError as e:
            if str(e) == "no orders":
                return []
            else:
                raise APIError(str(e))
        return self.orders_from_dict(r)
    
    def order_detail(self, order_id, auth):
        r = self.private_json("OrderInfo", auth, params={"order_id":order_id})
        return self.orders_from_dict(r)
    
    def order_create(self, order, auth):
        if not order.order_type in self.ORDER_TYPES:
            raise APIError("Invalid order type.")
            
        params = {
            "pair":order.pair,
            "type":order.direction,
            "rate":order.price,
            "amount":order.amount
        }
        r = self.private_json("Trade", auth, params=params)
        return r["order_id"]
    
    def order_delete(self, order_id, auth):
        self.private_json("CancelOrder", auth, params={"order_id":order_id})
    
    def orders_from_dict(self, data):
        orders = []
        for order_id, order in data.iteritems():
            amount = order["amount"]
            amount_remaining = None
            if order.get("start_amount"):
                amount_remaining = amount
                amount = order["start_amount"]
            orders.append(Order(order["pair"], Order.LIMIT_ORDER, order["type"], amount, price=order["rate"], order_id=int(order_id), amount_remaining=amount_remaining))
        return orders