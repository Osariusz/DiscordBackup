import discord
from Channel import Channel
from OwnerCog import OwnerCog
from discord.ext import commands
import asyncio


class Bot(commands.Bot):

    def __init__(self,intents):
        super().__init__(command_prefix="$",intents=intents)
        self.backuped_channels = []
        self.add_cog(OwnerCog(self))

    def check_if_id_present(self, id : int):
        for channel in self.backuped_channels:
            if(str(channel.id) == str(id)):
                return True
        return False

    async def try_add_backuped_channel(self, id : int):
        if(self.check_if_id_present(id)):
            return False
        discord_channel = await self.fetch_channel(id)
        bot_channel = Channel(self)
        bot_channel.copy_from_channel(discord_channel)
        self.backuped_channels.append(bot_channel)
        return True

    def backup_channels(self):
        for channel in self.backuped_channels:
            asyncio.create_task(channel.backup())

