import discord
from discord.ext import commands

import random


def create_bot(bot_prefix, self_bot):
    client = commands.Bot(command_prefix=bot_prefix, self_bot=self_bot)

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name='Doto'))
        print('We have logged in as {}'.format(client.user))

    @client.command(name='roll',
                    description="This command accepts two parameters, start number and end number. Randoms both",
                    brief="Rolls a random number (Default 1-100)",
                    aliases=['roll_die', 'roll_dice'])
    async def roll(ctx, start=1, end=100):
        result = random.randint(int(start), int(end))
        await ctx.send(str(result) + ctx.message.author.mention)

    @roll.error
    async def roll_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments provided")

    return client
