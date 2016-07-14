from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from utils.views import *

from prices.interface import prices_get

# Create your views here.
class GetPrices(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        if request.GET.get("exchange") and request.GET.get("pair"):
            if request.GET.get("days"):
                num_prices = int(request.GET["days"]) * 1440
            else:
                num_prices = None
                
            result = prices_get(request.GET["exchange"], request.GET["pair"], num_prices=num_prices)
            if result != None:
                return r_success(result)
            else:
                return r_failure("Exchange/trading pair combination not found.")
        else:
            return r_failure("Must specify 'exchange' and 'pair' parameters.")