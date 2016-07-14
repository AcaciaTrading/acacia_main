from django.conf import settings

from requests.auth import AuthBase
from exchanges.models import Nonce
import urllib
import hashlib
import hmac
import time
import base64

class BTCeAuth(AuthBase):
    def __init__(self, key, secret, params):
        self.key = key
        self.secret = secret
        self.params = params
        
    def __call__(self, r):
        r.headers["Content-type"] = "application/x-www-form-urlencoded"
        r.headers["Key"] = self.key
        
        h = hmac.new(self.secret, digestmod=hashlib.sha512)
        url_params = urllib.urlencode(self.params)
        h.update(url_params)
        sign = h.hexdigest()
        r.headers["Sign"] = sign
        return r
    
    
class CryptsyAuth(AuthBase):
    def __init__(self, key, secret, params):
        self.key = key
        self.secret = secret
        self.params = params
        
    def __call__(self, r):
        r.headers["Content-type"] = "application/x-www-form-urlencoded"
        r.headers["Key"] = self.key
        
        h = hmac.new(self.secret, digestmod=hashlib.sha512)
        url_params = urllib.urlencode(self.params)
        h.update(url_params)
        sign = h.hexdigest()
        r.headers["Sign"] = sign
        print r.headers
        return r
    
    
class BitstampAuth(object):
    def update_params(self, params, key, secret, user_id):
        nonce = get_nonce("Bitstamp_" + str(user_id) + key + secret)
        message = str(nonce) + str(user_id) + key
        sign = hmac.new(secret, msg=message, digestmod=hashlib.sha256)
        sign = sign.hexdigest().upper()
        params["key"] = key
        params["signature"] = sign
        params["nonce"] = nonce
        return params
    
class KrakenAuth(object):
    def __init__(self, key, secret, method, params):
        self.key = key
        self.secret = secret
        self.method = method
        self.params = params
        
    def __call__(self, r):
        r.headers["Content-type"] = "application/x-www-form-urlencoded"
        r.headers["API-Key"] = self.key.replace(" ", "+")
        
        urlpath = '/0/private/' + self.method
        
        postdata = urllib.urlencode(self.params)
        #print "params:", self.params
        #print "nonce:", self.params["nonce"]
        message = urlpath + hashlib.sha256(str(self.params["nonce"]) + postdata).digest()
        #print message
        signature = hmac.new(base64.b64decode(self.secret.replace(" ", "+")), message, hashlib.sha512)
        r.headers["API-Sign"] = base64.b64encode(signature.digest())
        
        #print r.headers
        return r
        
        
def get_nonce(auth_string):
    timestamp = int(time.time())
    if Nonce.objects.filter(auth=auth_string).exists():
        nonce_object = Nonce.objects.get(auth=auth_string)
        if timestamp - 30 > nonce_object.nonce:
            nonce_object.nonce = timestamp
        else:
            nonce_object.nonce += 1
    else:
        nonce_object = Nonce(auth=auth_string)
        nonce_object.nonce = timestamp
    nonce_object.save()
    #print "nonce", nonce_object.nonce, " for", auth_string
    return nonce_object.nonce