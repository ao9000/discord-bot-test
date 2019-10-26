from bot.helper_functions import url_join

import requests
import os
import json

# Base url
discord_base_url = "https://discordapp.com/api"
opendota_base_url = "https://api.opendota.com/api"


# Discord API
def discord_api_get_user_profile(version, discord_id):
    url = url_join(discord_base_url, "v{}".format(version), "users/{}/profile".format(discord_id))

    header = {'Authorization': os.getenv('discord_token_user', None)}
    request = requests.get(url=url, headers=header)

    response = json.loads(request.text)
    return response


# OpenDota API
def opendota_api_get_player_profile(steam_id_32):
    url = url_join(opendota_base_url, "players/{}".format(steam_id_32))

    req = requests.models.PreparedRequest()
    params = {'api_key': os.getenv("opendota_api_key", None)}
    req.prepare_url(url=url, params=params)

    request = requests.get(url=req.url)

    response = json.loads(request.text)
    return response
