from utils.client import api_get
from main.views import create_token_if_not_exists

def cur_convert(amount, from_cur, to_cur, pairs, order):
    if from_cur == to_cur:
        return amount
    else:
        create_token_if_not_exists(order.user)
        
        f_pair = from_cur + "_" + to_cur
        b_pair = to_cur + "_" + from_cur
        if f_pair in pairs:
            ticker = api_get(
                "exchanges:pair_detail",
                order.user.auth_token.key,
                {"exchange":order.exchange},
                args=(f_pair,)
            )["result"]["ticker"]
            return 1.0 * amount * ticker["bid"]
        elif b_pair in pairs:
            ticker = api_get(
                "exchanges:pair_detail",
                order.user.auth_token.key,
                {"exchange":order.exchange},
                args=(b_pair,)
            )["result"]["ticker"]
            return 1.0 * amount / ticker["ask"]
        else:
            raise Exception("Failed to obtain min order amount.")