import json
import time
import discord
import nltk

from bot.exceptions import APIError, APIMonthlyLimitReachedError

# NLTK resources
nltk.download('punkt')


# Decorators
# API handlers
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


# Pagination handlers
def PaginationHandlerMeta(character_limit):
    def PaginationHandler(func):
        async def func_wrapper(*args, **kwargs):
            # Await coroutine response
            response = await func(*args, **kwargs)

            for arg in args:
                if isinstance(arg, discord.ext.commands.context.Context):
                    ctx = arg
                    break
            # Text tokenization
            if len(response) > character_limit:
                response_tokenized = nltk.word_tokenize(response)

            # Construct paginated response
                start_index = 0
                for end_index, _ in enumerate(response_tokenized, start=1):
                    if len(" ".join([word for word in response_tokenized[start_index:end_index]])) > character_limit:
                        await ctx.send(" ".join([word for word in response_tokenized[start_index:end_index-1]]))
                        start_index = end_index - 1
                    elif end_index == len(response_tokenized):
                        await ctx.send(" ".join([word for word in response_tokenized[start_index:end_index]]))
                return
            else:
                return await ctx.send(response)

        return func_wrapper
    return PaginationHandler
