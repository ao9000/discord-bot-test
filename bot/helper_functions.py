import urllib.parse
import functools
import math


# Steam
def steam_id_64_to_steam_id_32(steam_id_64):
    steam_id_64_binary = "{0:b}".format(int(steam_id_64))
    steam_id_32_binary = str(steam_id_64_binary)[-31:]
    steam_id_32 = int(steam_id_32_binary, 2)

    return steam_id_32


# OpenDota
def opendota_rank_tier_to_medal_name(rank_tier, leaderboard_rank):
    rank_tier_dict = {
        "0": "Uncalibrated",
        "11": "Herald [1]",
        "12": "Herald [2]",
        "13": "Herald [3]",
        "14": "Herald [4]",
        "15": "Herald [5]",
        "16": "Herald [6]",
        "17": "Herald [7]",
        "21": "Guardian [1]",
        "22": "Guardian [2]",
        "23": "Guardian [3]",
        "24": "Guardian [4]",
        "25": "Guardian [5]",
        "26": "Guardian [6]",
        "27": "Guardian [7]",
        "31": "Crusader [1]",
        "32": "Crusader [2]",
        "33": "Crusader [3]",
        "34": "Crusader [4]",
        "35": "Crusader [5]",
        "36": "Crusader [6]",
        "37": "Crusader [7]",
        "41": "Archon [1]",
        "42": "Archon [2]",
        "43": "Archon [3]",
        "44": "Archon [4]",
        "45": "Archon [5]",
        "46": "Archon [6]",
        "47": "Archon [7]",
        "51": "Legend [1]",
        "52": "Legend [2]",
        "53": "Legend [3]",
        "54": "Legend [4]",
        "55": "Legend [5]",
        "56": "Legend [6]",
        "57": "Legend [7]",
        "61": "Ancient [1]",
        "62": "Ancient [2]",
        "63": "Ancient [3]",
        "64": "Ancient [4]",
        "65": "Ancient [5]",
        "66": "Ancient [6]",
        "67": "Ancient [7]",
        "71": "Divine [1]",
        "72": "Divine [2]",
        "73": "Divine [3]",
        "74": "Divine [4]",
        "75": "Divine [5]",
        "76": "Divine [6]",
        "77": "Divine [7]",
        "80": "Immortal [{}]".format(leaderboard_rank if leaderboard_rank is not math.inf else None)
    }

    return rank_tier_dict[str(rank_tier)]


# Others
def url_join(*args):
    args = list(args)
    # Ensure trailing slash behind
    for index, arg in enumerate(args):
        if arg[-1:] != "/":
            args[index] = arg + "/"

    return functools.reduce(urllib.parse.urljoin, args).rstrip("/")
