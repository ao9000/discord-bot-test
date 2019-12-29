from bot import create_bot
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path('.env'))

bot_prefix = ("!", "?")
client = create_bot(bot_prefix=bot_prefix, self_bot=False)

if __name__ == '__main__':
    client.run(os.getenv("discord_token_bot", None))
