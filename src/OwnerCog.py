import discord
from discord.ext import commands
import os
from Channel import Channel
from Reaction import Reaction
import json
from asyncio import sleep

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_channel(self,ctx,channel_id : int = None):
        if(channel_id == None):
            channel_id = ctx.channel.id

        success = await self.bot.try_add_backuped_channel(channel_id)
        if(success):
            await ctx.reply(f"Added {channel_id}")
        else:
            await ctx.reply(f"Failed to add {channel_id}")
    
    @commands.command()
    async def backup_channels(self,ctx):
        self.bot.backup_channels()
        await ctx.reply(f"Backuped channels: {[channel.name for channel in self.bot.backuped_channels]}")

    @commands.command()
    async def load_channel(self,ctx, channel_id : int = None):
        if(channel_id == None):
            channel_id = ctx.channel.id
        channel_file = f"{channel_id}.json"
        if(os.path.exists(channel_file)):
            channel = Channel(self.bot)
            with open(channel_file,"r",encoding="utf-8") as file:
                channel.load_messages(file.read())
            await channel.send_all_messages(ctx.channel)
        else:
            await ctx.reply(f"There is no backuped channel with id {channel_id}")