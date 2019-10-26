from bot.function import url_join

import requests
import os
import json

# Base url
discord_base_url = "https://discordapp.com/api"


# Discord API
def discord_api_get_user_profile(version, discord_id):
    url = url_join(discord_base_url, "v{}".format(version), "users/{}/profile".format(discord_id))

    header = {'Authorization': os.getenv('token_user', None)}
    request = requests.get(url=url, headers=header)

    response = json.loads(request.text)
    return response
