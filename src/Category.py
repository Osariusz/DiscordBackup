import discord
from Channel import Channel
import logging

class Category():

    def __init__(self,bot, backups_path: str):
        self.bot = bot
        self.id = 0
        self.channels: list[Channel] = []
        self.backups_path = backups_path

    def copy_from_category(self, category : discord.CategoryChannel):
        self.id = category.id
        self.name = category.name
        for discord_channel in category.channels:
            if isinstance(discord_channel, discord.TextChannel):
                channel = Channel(self.bot, self.backups_path)
                channel.copy_from_channel(discord_channel)
                self.channels.append(channel)

    async def backup(self):
        logging.getLogger().info(f"Backuping category {self.id}")
        for channel in self.channels:
            try:
                await channel.backup(category_path=str(self.id))
            except Exception as e:
                logging.getLogger().error(f"Can't backup channel {channel.id} in category {self.id} reason: {e}")