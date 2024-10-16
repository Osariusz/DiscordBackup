import asyncio
import logging
from typing import Optional

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

    def cog_check(self, ctx: discord.ApplicationContext) -> bool:
        result = ctx.author.id in self.bot.vars["allowed_users"]
        if not result:
            asyncio.create_task(ctx.respond("You are not allowed to use this command", ephemeral=True))
        return result

    @discord.command()
    async def add_channel(self,ctx: discord.ApplicationContext,channel_id_str : Optional[str]):
        channel_id: int
        if(channel_id_str is None):
            channel_id = ctx.channel.id
        else:
            channel_id = int(channel_id_str)

        success = await self.bot.try_add_backuped_id(channel_id)
        if(success):
            to_reply = f"Added {channel_id} "
            channel = self.bot.get_backuped_channel(channel_id)
            if(isinstance(channel,Channel)):
                to_reply += "to backuped channels"
            else:
                to_reply += "to backuped categories"

            await ctx.respond(to_reply)
        else:
            await ctx.respond(f"Failed to add {channel_id}")
    
    @discord.command()
    async def remove_channel(self, ctx: discord.ApplicationContext, channel_id_str : Optional[str]):
        channel_id: int
        if(channel_id_str is None):
            channel_id = ctx.channel_id
        else:
            channel_id = int(channel_id)

        channel = self.bot.get_backuped_channel(channel_id)
        if(channel == None):
            await ctx.respond(f"No channel {channel_id} in backups")
            return
        in_category = False
        if(not channel in self.bot.backuped_channels):
            in_category = True

        success = await self.bot.remove_channel_id(channel_id)

        if(success):
            to_reply = f"Removed {channel_id} "
            if(isinstance(channel, discord.CategoryChannel)):
                to_reply += "from backuped categories"
            elif(in_category):
                to_reply += "from backuped category (category translated to channels)"
            else:
                to_reply += "from backuped channels"
            await ctx.respond(to_reply)
        else:
            await ctx.respond(f"Failed to remove {channel_id}")

    @discord.command()
    async def remove_all_channels(self, ctx: discord.ApplicationContext):
        logging.getLogger().info("Removing all channels")
        await self.bot.remove_all_channels()
        await ctx.respond("Removed all channels")




    @discord.command()
    async def list_channels(self, ctx: discord.ApplicationContext):
        result = "backuped_channels: "
        for channel in self.bot.backuped_channels:
            result += f"{channel.id} "
        result += "\nbackuped categories: "
        for category in self.bot.backuped_categories:
            result += f"{category.id} " 
        await ctx.respond(result)

    @discord.command()
    async def list_channels_names(self, ctx: discord.ApplicationContext):
        result = "backuped_channels: "
        for channel in self.bot.backuped_channels:
            result += f"{channel.name} "
        result += "\nbackuped categories: "
        for category in self.bot.backuped_categories:
            result += f"{category.name} " 
        await ctx.respond(result)

    @discord.command()
    async def backup_channels(self,ctx: discord.ApplicationContext):
        await ctx.respond(f"Starting channels backup")
        start_time = datetime.datetime.now()
        await self.bot.backup_channels()
        end_time = datetime.datetime.now()
        if self.bot.get_start_date_update_after_backup():
            self.bot.set_start_date(start_time)
        await ctx.respond(f"Channels backup completed in {end_time-start_time}")

    #@discord.command()
    async def load_channel(self,ctx: discord.ApplicationContext, channel_id : Optional[str]):
        # TODO: fix loading channels
        return
        if(channel_id == None):
            channel_id = ctx.channel.id

        channel_id = int(channel_id)

        channel = self.bot.get_backuped_channel(int(channel_id))
        if(channel == None):
            discord_channel = await self.bot.fetch_channel(channel_id)
            if(not await self.bot.try_add_backuped_channel(discord_channel)):
                await ctx.respond(f"Can't load channel {channel_id}")
                return
        channel_file = self.bot.get_backuped_channel_file_path_no_categories(channel_id)
        if(os.path.exists(channel_file)):
            channel = Channel(self.bot)
            with open(channel_file,"r",encoding="utf-8") as file:
                channel.load_messages(file.read())
            await channel.send_all_messages(ctx.channel)
        else:
            await ctx.respond(f"There is no backuped channel with id {channel_id}")

    