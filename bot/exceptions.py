import json
import time


class APIError(Exception):
    pass


# Decorators
def APIHandler(func):
    def func_wrapper(*args, **kwargs):
        request = func(*args, **kwargs)
        if request.status_code == 200:
            return json.loads(request.text)
        elif request.status_code == 429:
            print("API limit reached, Waiting 1 minute")
            time.sleep(60)
            request = func(*args, **kwargs)
            return json.loads(request.text)
        else:
            raise APIError("Unknown API error")
    return func_wrapper
