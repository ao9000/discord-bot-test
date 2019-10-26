from bot.api import discord_api_get_user_profile, opendota_api_get_player_profile
from bot.helper_functions import steam_id_64_to_steam_id_32, opendota_rank_tier_to_medal_name

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
                    description="Displays the Dota 2 medal of members in the server sorted in descending order",
                    brief="Displays the Dota 2 medal of members in the server",
                    aliases=['dota2_member_medal'])
    async def dota2_server_medal(ctx):
        response_dict = {}

        members = ctx.guild.members
        for member in members:
            if not member.bot:
                user_object = discord_api_get_user_profile(os.getenv("discord_api_version", 6), member.id)

                connection_object = user_object['connected_accounts']
                if len(connection_object) != 0:
                    for connection in connection_object:
                        if connection['type'] == 'steam':
                            steam_id_64 = connection['id']
                            opendota_profile_object = opendota_api_get_player_profile(steam_id_64_to_steam_id_32(steam_id_64))
                            dota2_rank_tier = opendota_profile_object['rank_tier']
                            leaderboard_rank = opendota_profile_object['leaderboard_rank']
                            response_dict[member.name + "#" + member.discriminator] = [dota2_rank_tier if dota2_rank_tier else 0, leaderboard_rank if leaderboard_rank else math.inf]

        if not response_dict:
            await ctx.send("No members found" + ctx.message.author.mention)
        else:
            member_name_combined = ""
            medal_combined = ""
            for key, value in sorted(response_dict.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True):
                member_name_combined += key + '\n'
                medal_combined += opendota_rank_tier_to_medal_name(value[0], value[1]) + '\n'

                embed = discord.Embed(title="Medal Ranking", description="Dota 2 medal distribution in the server", color=0x00ff00)
                embed.set_footer(text='Updated on {}'.format(datetime.datetime.now()))
                embed.add_field(name="Discord Name", value=member_name_combined, inline=True)
                embed.add_field(name="Dota 2 Medal", value=medal_combined, inline=True)

            await ctx.send(ctx.message.author.mention, embed=embed)

    return client
