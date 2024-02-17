import discord
from Channel import Channel
import logging

class Category():

    def __init__(self,bot):
        self.bot = bot
        self.id = 0
        self.channels = []

    def copy_from_category(self, category : discord.CategoryChannel):
        self.id = category.id
        self.name = category.name
        for discord_channel in category.channels:
            channel = Channel(self.bot)
            channel.copy_from_channel(discord_channel)
            self.channels.append(channel)

    async def backup(self):
        logging.getLogger().info(f"Backuping category {self.id}")
        for channel in self.channels:
            try:
                await channel.backup(str(self.id))
            except Exception as e:
                logging.getLogger().error(f"Can't backup channel {channel.id} in category {self.id} reason: {e}")