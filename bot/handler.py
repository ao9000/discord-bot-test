import json
import time
import copy
import discord
import nltk
import functools

from bot.exceptions import APIError, APIMonthlyLimitReachedError, CharacterLimitExceededError
from bot.helper_functions import discord_create_embed_table

# NLTK resources
nltk.download('punkt')


# Decorators
# API handlers
def GeneralAPIHandler(func):
    @functools.wraps(func)
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
    @functools.wraps(func)
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
def PaginationHandlerMeta(arg):
    def PaginationHandler(func):
        @functools.wraps(func)
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
                        await ctx.send(" ".join([word for word in response_tokenized[start_index:end_index - 1]]))
                        start_index = end_index - 1
                    elif end_index == len(response_tokenized):
                        await ctx.send(" ".join([word for word in response_tokenized[start_index:end_index]]))
                return
            else:
                return await ctx.send(response)

        return func_wrapper

    if callable(arg):
        # No argument provided
        character_limit = 2000
        return PaginationHandler(arg)
    else:
        # Argument provided
        character_limit = arg
        return PaginationHandler


def EmbedPaginationHandlerMeta(table=False):
    def EmbedPaginationHandler(func):
        @functools.wraps(func)
        async def func_wrapper(*args, **kwargs):
            # Await coroutine response
            response = await func(*args, **kwargs)

            for arg in args:
                if isinstance(arg, discord.ext.commands.context.Context):
                    ctx = arg
                    break

            # Embed character limit checks
            # For reference - https://discordapp.com/developers/docs/resources/channel#embed-limits

            # Optional embed arguments
            if 'title' in response:
                if len(response['title']) > 256:
                    raise CharacterLimitExceededError("Embed title character limit exceeded")

            if 'description' in response:
                if len(response['description']) > 2048:
                    raise CharacterLimitExceededError("Embed description character limit exceeded")

            if 'column_value' in response:
                if len(response['column_value']) > 25:
                    raise CharacterLimitExceededError("Embed field object limit exceeded")

            if 'footer' in response:
                if len(response['footer']) > 2048:
                    raise CharacterLimitExceededError("Embed footer character limit exceeded")

            if 'author' in response:
                if len(response['author']) > 256:
                    raise CharacterLimitExceededError("Embed author name character exceeded")

            # Compulsory embed arguments
            if any(len(header) > 256 for header in response['column_header']):
                raise CharacterLimitExceededError("Embed column header character limit exceeded")
            elif any(len(value) > 1024 for value in response['column_value']):
                if table:
                    # Text tokenization (New line separator)
                    response['column_value'] = [value.split("\n") for value in response['column_value']]

                    # Construct paginated response
                    temp = list()
                    for row in zip(*response['column_value']):

                        if temp:
                            temp = ["{}\n{}".format(a, b) for a, b in zip(temp, list(row))]
                        else:
                            temp = list(row)

                        if any(len(value) > 1024 for value in temp):
                            # Removing last addition
                            temp = ["\n".join(word) for word in [col.split("\n")[:-1] for col in temp]]
                            embed = discord_create_embed_table(title=response.get("title", None),
                                                               column_header=response['column_header'],
                                                               column_value=[value for value in temp],
                                                               description=response.get("description", None),
                                                               footer=response.get("footer", None),
                                                               author=response.get("author", None)
                                                               )
                            await ctx.send(embed=embed)
                            # Retain overlapping row
                            temp = list(row)

                else:
                    # Text tokenization
                    response['column_value'] = [nltk.word_tokenize(value) for value in response['column_value']]

                    # Construct paginated response
                    for index, value in enumerate(copy.deepcopy(response['column_value']), start=0):
                        temp = list()
                        start_index = 0
                        for end_index, _ in enumerate(value, start=1):
                            if len(" ".join([word for word in value[start_index:end_index]])) > 1024:
                                temp.append(" ".join([word for word in value[start_index:end_index - 1]]))
                                start_index = end_index - 1
                            elif end_index == len(value):
                                temp.append(" ".join([word for word in value[start_index:end_index]]))
                        response['column_value'][index] = temp

                    for index in range(0, max(len(value) for value in response['column_value']) - 1):
                        embed = discord_create_embed_table(title=response.get("title", None),
                                                           column_header=response['column_header'],
                                                           column_value=[value[index] for value in response['column_value']],
                                                           description=response.get("description", None),
                                                           footer=response.get("footer", None),
                                                           author=response.get("author", None)
                                                           )
                        await ctx.send(embed=embed)

            else:
                embed = discord_create_embed_table(title=response.get("title", None),
                                                   column_header=response['column_header'],
                                                   column_value=response['column_value'],
                                                   description=response.get("description", None),
                                                   footer=response.get("footer", None),
                                                   author=response.get("author", None)
                                                   )
                await ctx.send(embed=embed)

        return func_wrapper
    return EmbedPaginationHandler
