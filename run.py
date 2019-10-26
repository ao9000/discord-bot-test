from bot import create_bot
import os

bot_prefix = ("!", "?")
client = create_bot(bot_prefix=bot_prefix, self_bot=False)

if __name__ == '__main__':
    client.run(os.getenv("token_bot", None))
