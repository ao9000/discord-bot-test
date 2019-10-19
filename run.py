from bot import create_bot
import os

bot_prefix = ("!", "?")
client = create_bot(bot_prefix=bot_prefix, self_bot=False)


client.run(os.getenv("bot_token", None))
