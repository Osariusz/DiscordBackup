import discord
from discord.ext import commands
import os
from Channel import Channel
from Reaction import Reaction
import json
from asyncio import sleep
import datetime

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self,ctx):
        result = ctx.author.id in self.bot.vars["allowed_users"]
        if(not result):
            await ctx.reply("You are not allowed to use this command")
        return result

    @commands.command()
    async def add_channel(self,ctx,channel_id : int = None):
        if(channel_id == None):
            channel_id = ctx.channel.id

        channel = await self.bot.fetch_channel(channel_id)
        success = await self.bot.try_add_backuped_channel(channel)
        if(success):
            to_reply = f"Added {channel_id} "
            if(isinstance(channel,discord.CategoryChannel)):
                to_reply += "to backuped categories"
            else:
                to_reply += "to backuped channels"

            await ctx.reply(to_reply)
        else:
            await ctx.reply(f"Failed to add {channel_id}")
    
    @commands.command()
    async def list_channels(self, ctx):
        result = "backuped_channels: "
        for channel in self.bot.backuped_channels:
            result += f"{channel.id} "
        result += "\nbackuped categories: "
        for category in self.bot.backuped_categories:
            result += f"{category.id} " 
        await ctx.reply(result)

    @commands.command()
    async def backup_channels(self,ctx):
        await ctx.reply(f"Starting channels backup")
        start_time = datetime.datetime.now()
        await self.bot.backup_channels()
        end_time = datetime.datetime.now()
        await ctx.reply(f"Channels backup completed in {end_time-start_time}")

    @commands.command()
    async def load_channel(self,ctx, channel_id : int = None):
        if(channel_id == None):
            channel_id = ctx.channel.id
        channel = self.bot.get_backuped_channel(int(channel_id))
        if(channel == None):
            discord_channel = await self.bot.fetch_channel(channel_id)
            if(not await self.bot.try_add_backuped_channel(discord_channel)):
                await ctx.reply(f"Can't load channel {channel_id}")
                return
        channel_file = self.bot.get_backuped_channel_file_path_no_categories(channel_id)
        if(os.path.exists(channel_file)):
            channel = Channel(self.bot)
            with open(channel_file,"r",encoding="utf-8") as file:
                channel.load_messages(file.read())
            await channel.send_all_messages(ctx.channel)
        else:
            await ctx.reply(f"There is no backuped channel with id {channel_id}")

    