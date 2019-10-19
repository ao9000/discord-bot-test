import discord
from discord.ext import commands


def create_bot(bot_prefix, self_bot):
    client = commands.Bot(command_prefix=bot_prefix, self_bot=self_bot)

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    return client
