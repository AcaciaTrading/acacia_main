import json
import boto
from boto.s3.key import Key

MAX_CACHE_TIME = 30

# Local file settings
DATA_DIR = "prices/price_data/"
SEPARATOR = "_-_"
MAX_PRICES = 129600

# AWS S3 settings
BUCKET_NAME = "acacia-prices"


def prices_get(exchange, pair, num_prices=None, price_ratio=1, cached=True):
    filename = get_filename(exchange, pair)
    if cached == True:
        from django.core.cache import cache
        text = cache.get(filename)
    else:
        text = None
        
    if text == None:
        try:
            text = get_s3_text(filename)
            if cached == True:
                cache.set(filename, text, MAX_CACHE_TIME)
        except Exception as e:
            print str(e)
            return None
        
    result = json.loads(text)
    
    result = result[0::price_ratio]
    if num_prices != None:
        return result[:num_prices]
    else:
        return result

def prices_append(exchange, pair, value):
    prices = prices_get(exchange, pair, cached=False)
    
    if prices == None:
        prices = []
    prices = [value] + prices
    if len(prices) > MAX_PRICES:
        prices = prices[len(prices) - MAX_PRICES:]
        
    filename = get_filename(exchange, pair)
    set_s3_from_string(filename, json.dumps(prices))

def get_s3_text(filename):
    k = get_s3_key()
    k.key = filename
    return k.get_contents_as_string()

def set_s3_from_string(filename, data):
    k = get_s3_key()
    k.key = filename
    k.set_contents_from_string(data)
    

def get_s3_key():
    c = boto.connect_s3()
    b = c.get_bucket(BUCKET_NAME)
    return Key(b)
    
def get_filename(exchange, pair):
    return DATA_DIR + exchange + SEPARATOR + pair + ".json"