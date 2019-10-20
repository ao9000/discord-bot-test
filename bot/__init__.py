import discord
from discord.ext import commands

import random


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
    

    return client
