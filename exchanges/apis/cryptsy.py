from exchanges.abstract import *
from auths import CryptsyAuth, get_nonce

# Cryptsy is currently offline and may never come back on
# will continue integration process if they re-enable trading
# http://blog.cryptsy.com/post/137323646202/announcement

class Cryptsy(Exchange):
    BASE_URL = "https://api.cryptsy.com/api/v2/"
    PAIRS = ()
    PAIRS_IDS = {}
    IDS_PAIRS = {}
    FEES = (
        {"amount":0, "fee":0.0},
    )
    FEES_CUR = "btc"
    ORDER_TYPES = (
        Order.LIMIT_ORDER,
    )
    MIN_ORDER = 0.00000001
    MIN_ORDER_CUR = "btc"
    
    def __init__(self):
        self.make_pair_list()
    
    def public_json(self, url):
        r = requests.get(self.BASE_URL + url)
        r = r.json()
        if r.get("error"):
            raise APIError(r["error"])
        return r["data"]
    
    def private_json(self, method, url, auth, params={}):
        params["nonce"] = get_nonce("Cryptsy_" + auth[0] + auth[1])
        if method == "get":
            r = requests.get(self.BASE_URL + url, params=params, auth=CryptsyAuth(auth[0], auth[1], params))
        elif method == "delete":
            r = requests.delete(self.BASE_URL + url, data=params, auth=CryptsyAuth(auth[0], auth[1], params))
        else:
            r = requests.post(self.BASE_URL + url, data=params, auth=CryptsyAuth(auth[0], auth[1], params))
        r = r.json()
        if r["success"] == False:
            raise APIError(r["error"])
        return r["data"]
    
    def make_pair_list(self):
        r = self.public_json("markets")
        pairs = []
        for entry in r:
            pair_name = self.pair_normal(entry["label"])
            pairs.append(pair_name)
            self.PAIRS_IDS[pair_name] = entry["id"]
            self.IDS_PAIRS[entry["id"]] = entry["label"]
        self.PAIRS = pairs
    
    def pair_normal(self, pair):
        return pair.replace("/", "_").lower()
    
    def pair_detail(self, pair):
        if not pair in self.PAIRS:
            raise APIError("Invalid pair name: %s" % self.PAIRS)
            
        pair_id = self.PAIRS_IDS[pair]
        r_ticker = self.public_json("markets/" + pair_id + "/ticker")
        r_market = self.public_json("markets/" + pair_id + "")
        ticker = Ticker(
            low=r_market["24hr"]["price_low"], high=r_market["24hr"]["price_high"], average=None,
            bid=r_ticker["bid"], ask=r_ticker["ask"], last=r_market["last_trade"]["price"]
        )
        volume = r_market["24hr"]["volume"]
        
        r = self.public_json("markets/" + pair_id + "/orderbook")
        bids = [(x["price"], x["quantity"],) for x in r["buyorders"]]
        asks = [(x["price"], x["quantity"],) for x in r["sellorders"]]
        orderbook = OrderBook(bids, asks)
        return Pair(ticker, volume, orderbook, self.FEES)
    
    def pair_ticker(self, pair):
        pair_id = self.PAIRS_IDS[pair]
        r_ticker = self.public_json("markets/" + pair_id + "/ticker")
        r_market = self.public_json("markets/" + pair_id + "/")
        return Ticker(
            low=r_market["24hr"]["price_low"], high=r_market["24hr"]["price_high"], average=None,
            bid=r_ticker["bid"], ask=r_ticker["ask"], last=r_market["last_trade"]["price"]
        )
        
    def user_detail(self, auth):
        r = self.private_json("get", "balances/", auth)
        r = r["available"]
        
        balances = {}
        for cur_id, amount in r.items():
            if cur_id in self.IDS_PAIRS:
                balances[
                    self.pair_normal(self.IDS_PAIRS[cur_id])
                ] = float(amount)
            
        r = self.private_json("get", "tradehistory/", auth)
        raise Exception("I need a trade history for this!")
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
        perm = {}
        for value in APIKey.PERMISSIONS:
            perm[value] = 1
        
        return APIKey(perm)
    
    def order_list(self, auth):
        # unfinished
        try:
            r = self.private_json("ActiveOrders", auth)
        except APIError as e:
            if str(e) == "no orders":
                return []
            else:
                raise APIError(str(e))
        return self.orders_from_dict(r)
    
    def order_detail(self, order_id, auth):
        # unfinished
        r = self.private_json("OrderInfo", auth, params={"order_id":order_id})
        return self.orders_from_dict(r)
    
    def order_create(self, order, auth):
        # unfinished
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
        # unfinished
        self.private_json("delete" "order/" + order_id, auth)
    
    def orders_from_dict(self, data):
        # unfinished
        orders = []
        for order_id, order in data.iteritems():
            amount = order["amount"]
            amount_remaining = None
            if order.get("start_amount"):
                amount_remaining = amount
                amount = order["start_amount"]
            orders.append(Order(order["pair"], Order.LIMIT_ORDER, order["type"], amount, price=order["rate"], order_id=int(order_id), amount_remaining=amount_remaining))
        return orders