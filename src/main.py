from types import SimpleNamespace
import discord
import json
from Message import Message
from MessageData import MessageData
from dotenv import load_dotenv
import os
from Bot import Bot
from OwnerCog import OwnerCog

if(__name__ == "__main__"):

    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(intents)
    
    bot.run(os.getenv("DISCORD_TOKEN"))
