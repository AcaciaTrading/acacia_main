from acacia_main.settings import BASE_URL
from django.core.urlresolvers import reverse

import requests

def api_get(method, auth_token, params, args=None):
    r = requests.get(
        BASE_URL + reverse(method, args=args),
        headers=auth_header(auth_token),
        params=params
    )
    r = r.json()
    if r["success"] == False:
        raise APIError(r["error"])
    return r
    
def api_post(method, auth_token, params):
    r = requests.post(
        BASE_URL + reverse(method),
        headers=auth_header(auth_token),
        data=params
    )
    r = r.json()
    if r["success"] == False:
        raise APIError(r["error"])
    return r

def order_params(order):
    return {
        "exchange":order.exchange,
        "api_key":order.api_key,
        "api_secret":order.api_secret,
        "api_id":order.api_id
    }

def auth_from_order(order):
    return (str(order.api_key), str(order.api_secret), str(order.api_id),)

def auth_header(auth_token):
    return {'authorization':'Token %s' % auth_token}

class APIError(Exception):
    pass