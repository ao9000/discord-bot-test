from bot.helper_functions import url_join
from bot.handler import GeneralAPIHandler, OpenDotaAPIHandler

import requests
import os

# Base url
discord_base_url = "https://discordapp.com/api"
steam_base_url = "https://api.steampowered.com"
opendota_base_url = "https://api.opendota.com/api"


# Discord API
@GeneralAPIHandler
def discord_api_get_user_profile(version, discord_id):
    url = url_join(discord_base_url, "v{}".format(version), "users/{}/profile".format(discord_id))

    header = {'Authorization': os.getenv('discord_token_user', None)}
    request = requests.get(url=url, headers=header)

    return request

# Steam API
@GeneralAPIHandler
def steam_api_get_current_player_count(version, app_id):
    url = url_join(steam_base_url, "ISteamUserStats/GetNumberOfCurrentPlayers/v{}".format(version))

    req = requests.models.PreparedRequest()
    params = {'key': os.getenv("steam_api_key", None), 'appid': app_id}
    req.prepare_url(url=url, params=params)

    request = requests.get(url=req.url)

    return request


# OpenDota API
@OpenDotaAPIHandler
def opendota_api_get_player_profile(steam_id_32):
    url = url_join(opendota_base_url, "players/{}".format(steam_id_32))

    req = requests.models.PreparedRequest()
    params = {'api_key': os.getenv("opendota_api_key", None)}
    req.prepare_url(url=url, params=params)

    request = requests.get(url=req.url)

    return request
