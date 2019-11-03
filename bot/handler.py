import json
import time

from bot.exceptions import APIError, APIMonthlyLimitReachedError


# Decorators
def GeneralAPIHandler(func):
    def func_wrapper(*args, **kwargs):
        request = func(*args, **kwargs)
        if request.status_code == 200:
            return json.loads(request.text)
        elif request.status_code == 429:
            print("API limit reached for a minute, Waiting 1 minute")
            time.sleep(60)
            request = func(*args, **kwargs)
            return json.loads(request.text)
        else:
            raise APIError("Unknown API error")
    return func_wrapper


def OpenDotaAPIHandler(func):
    def func_wrapper(*args, **kwargs):
        request = func(*args, **kwargs)
        if request.status_code == 200:
            return json.loads(request.text)
        elif request.status_code == 429 and request.headers['X-Rate-Limit-Remaining-Minute'] < 0:
            print("API limit reached for a minute, Waiting 1 minute")
            time.sleep(60)
            request = func(*args, **kwargs)
            return json.loads(request.text)
        elif request.status_code == 429 and request.headers['X-Rate-Limit-Remaining-Month'] < 0:
            print("API limit reached for the month")
            raise APIMonthlyLimitReachedError("API limit reached for the month")
        else:
            raise APIError("Unknown API error")

    return func_wrapper
