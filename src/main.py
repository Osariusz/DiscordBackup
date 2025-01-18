from types import SimpleNamespace
import discord
import json
from Message import Message
from MessageData import MessageData
from dotenv import load_dotenv
import os
from Bot import Bot
from OwnerCog import OwnerCog
import logging

if(__name__ == "__main__"):

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting bot")

    load_dotenv()

    intents = discord.Intents.all()
    intents.message_content = True

    bot = Bot(intents)
    
    bot.run(os.getenv("DISCORD_TOKEN"))
