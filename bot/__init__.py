from bot.api import discord_api_get_user_profile, opendota_api_get_player_profile, steam_api_get_current_player_count, \
    opendota_api_get_mmr_distribution
from bot.helper_functions import steam_id_64_to_steam_id_32, opendota_rank_tier_to_medal_name, \
    discord_create_embed_table
from bot.handler import PaginationHandlerMeta, EmbedPaginationHandlerMeta

import discord
from discord.ext import commands
import random
import os
import datetime
import math


def create_bot(bot_prefix, self_bot):
    client = commands.Bot(command_prefix=bot_prefix, self_bot=self_bot)

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name='Doto'))
        print('We have logged in as {}'.format(client.user))

    # Basic commands
    @client.command(name='roll',
                    description="This command accepts two arguments, start number and end number. Randoms both",
                    brief="Rolls a random number (Default 1-100)",
                    aliases=['roll_die', 'roll_dice'])
    async def roll(ctx, start=1, end=100):
        result = random.randint(int(start), int(end))
        await ctx.send(str(result) + ctx.message.author.mention)

    @roll.error
    async def roll_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments provided" + ctx.message.author.mention)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Invalid range provided" + ctx.message.author.mention)

    @client.command(name='flip',
                    description="This command flips a coin and returns Heads or Tails",
                    brief="Returns Heads or Tails.",
                    aliases=['flip_coin'])
    async def flip(ctx):
        coin = ['Heads', 'Tails']
        result = random.choice(coin)
        await ctx.send(result + ctx.message.author.mention)

    @client.command(name='random',
                    description="This command accepts an unlimited amount of arguments to random",
                    brief="Randoms choices provided by the user",
                    aliases=['random_choice'])
    async def random_choice(ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide arguments for me to random" + ctx.message.author.mention)
        else:
            result = random.choice(list(args))
            await ctx.send(str(result) + ctx.message.author.mention)

    # Game related commands
    @client.command(name='dota2_server_medal',
                    description="Using Discord-OpenDota integration to retrieve the rank of members in the server",
                    brief="Displays the server medal ranking chart",
                    aliases=['dota2_member_medal'])
    @EmbedPaginationHandlerMeta(table=True)
    async def dota2_server_medal(ctx):
        response_dict = {}

        members = client.get_all_members()
        # members = ctx.guild.members
        for member in members:
            if not member.bot:
                user_object = discord_api_get_user_profile(os.getenv("discord_api_version", 6), member.id)

                connection_object = user_object['connected_accounts']
                if len(connection_object) != 0:
                    for connection in connection_object:
                        if connection['type'] == 'steam':
                            steam_id_64 = connection['id']
                            opendota_profile_object = opendota_api_get_player_profile(
                                steam_id_64_to_steam_id_32(steam_id_64))
                            dota2_rank_tier = opendota_profile_object['rank_tier']
                            leaderboard_rank = opendota_profile_object['leaderboard_rank']
                            response_dict[member.name + "#" + member.discriminator] = [
                                dota2_rank_tier if dota2_rank_tier else 0,
                                leaderboard_rank if leaderboard_rank else math.inf]

        if not response_dict:
            return {
                "title": "Medal Ranking",
                "column_header": ["Error"],
                "column_value": ["No member data found"],
                "description": "Dota 2 medal distribution in the server",
                "footer": "Updated on {}".format(datetime.datetime.now())
            }

        else:
            member_names = ""
            medals = ""
            for key, value in sorted(response_dict.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True):
                member_names += key + '\n'
                medals += opendota_rank_tier_to_medal_name(value[0], value[1]) + '\n'

            column_value = [member_names, medals]
            column_header = ["Discord name", "Medal"]

            return {
                "title": "Medal Ranking",
                "column_header": column_header,
                "column_value": column_value,
                "description": "Dota 2 medal distribution in the server",
                "footer": "Updated on {}".format(datetime.datetime.now())
            }

    @client.command(name='dota2_player_count',
                    description="Using the official Valve API, retrieve the current number of players on Dota 2",
                    brief="Displays the Dota 2 player count")
    @PaginationHandlerMeta
    async def dota2_current_player_count(ctx):
        player_count = steam_api_get_current_player_count(os.getenv("steam_api_version", 1), 570)['response'][
            'player_count']
        return "There is currently {:,} players in Dota 2".format(player_count)

    @client.command(name='dota2_mmr_dist_country',
                    description="Using the OpenDota API, retrieve the mmr distribution for each country and sort them in descending order",
                    brief="Displays the Dota 2 mmr distribution by country")
    @EmbedPaginationHandlerMeta(table=True)
    async def dota2_mmr_dist_country(ctx):
        mmr_dist_list = opendota_api_get_mmr_distribution()['country_mmr']['rows']

        if not mmr_dist_list:
            return {
                "title": "Country MMR distribution",
                "column_header": ["Error"],
                "column_value": ["No data found"],
                "description": "Dota 2 MMR distribution by country",
                "footer": "Updated on {}".format(datetime.datetime.now())
            }

        else:
            country_names = ""
            country_avg_mmr = ""
            for country_mmr_dict in sorted(mmr_dist_list, key=lambda x: x['avg'], reverse=True):
                country_names += country_mmr_dict['common'] + '\n'
                country_avg_mmr += country_mmr_dict['avg'] + '\n'

            column_value = [country_names, country_avg_mmr]
            column_header = ["Country", "Avg MMR"]

            return {
                "title": "Country MMR distribution",
                "column_header": column_header,
                "column_value": column_value,
                "description": "Dota 2 MMR distribution by country",
                "footer": "Updated on {}".format(datetime.datetime.now())
            }

    return client
