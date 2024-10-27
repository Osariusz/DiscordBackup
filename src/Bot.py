import datetime
import shutil
from time import sleep
from tokenize import String
import discord
from Channel import Channel
from OwnerCog import OwnerCog
from discord.ext import commands
import asyncio
import os
import json
from Category import Category
import logging
from enum import Enum
from VariableTypeEnum import VariableTypeEnum
import VarsManager

class Bot(commands.Bot):

    def __init__(self,intents):
        super().__init__(intents=intents)
        self.vars_manager = VarsManager()
        asyncio.ensure_future(self.load_backuped_ids())
        self.backuped_channels = []
        self.backuped_categories = []
        self.add_cog(OwnerCog(self))

    async def translate_category_to_channels(self, category : discord.CategoryChannel):
        self.backuped_categories.remove(category)
        await self.add_channels_to_backups(category.channels)

    async def remove_channel_id(self, id):
        channel = self.get_backuped_channel(id)
        return await self.remove_channel(channel)

    async def get_remove_result(self, channel) -> bool:
        if(channel == None):
            logging.getLogger().error(f"No channel with id {channel.id}")
            return False
        if(channel in self.backuped_channels):
            self.backuped_channels.remove(channel)
            return True
        elif(channel in self.backuped_categories):
            self.backuped_categories.remove(channel)
            return True
        else:
            for category in self.backuped_categories:
                if(channel in category.channels):
                    await self.translate_category_to_channels(category)
                    self.backuped_channels.remove(channel)
                    break
            return True
        
    async def remove_channel(self, channel) -> bool:
        result = await self.get_remove_result(channel)
        self.update_backuped_var()
        return result

    async def remove_all_channels(self):
        self.backuped_channels.clear()
        self.backuped_categories.clear()
        self.update_backuped_var()

    def get_backuped_channel_file_path_no_categories(self, id : int):
        for channel in self.backuped_channels:
            if(channel.id == id):
                return channel.channel_file()
        for category in self.backuped_categories:
            if(category.id == id):
                raise Exception("No categories allowed")
            for channel in category.channels:
                if(channel.id == id):
                    return channel.channel_file(str(category.id))
        return None

    def get_backuped_channel(self, id: int):
        for channel in self.backuped_channels:
            if(channel.id == id):
                return channel
        for category in self.backuped_categories:
            if(id == category.id):
                return category
            for channel in category.channels:
                if(channel.id == id):
                    return channel
        return None

    async def load_backuped_ids(self):
        if(VariableTypeEnum.BACKUPED_CHANNELS in self.vars):
            for channel_id in self.vars[VariableTypeEnum.BACKUPED_CHANNELS]:
                await self.try_add_backuped_id(channel_id)
        if(VariableTypeEnum.BACKUPED_CATEGORIES in self.vars):
            for category_id in self.vars[VariableTypeEnum.BACKUPED_CATEGORIES]:
                await self.try_add_backuped_id(category_id)

    def get_start_date_update_after_backup(self) -> bool:
        return self.vars_manager.vars[VariableTypeEnum.INCREASE_START_DATE_AFTER_BACKUP] == "True"

    def set_start_date(self, start_date: datetime.datetime) -> None:
        self.vars_manager.vars[VariableTypeEnum.START_DATE] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        self.vars_manager.update_var(VariableTypeEnum.START_DATE)

    def update_backuped_var(self):
        self.vars[VariableTypeEnum.BACKUPED_CHANNELS] = [channel.id for channel in self.backuped_channels]
        self.vars[VariableTypeEnum.BACKUPED_CATEGORIES] = [category.id for category in self.backuped_categories]
        self.update_var(VariableTypeEnum.BACKUPED_CHANNELS)
        self.update_var(VariableTypeEnum.BACKUPED_CATEGORIES)

    def check_if_id_present(self, id : int):
        result = self.get_backuped_channel(id)
        if(result == None):
            return False
        return True

    async def add_channels_to_backups(self, channels : list):
        try:
            for channel in channels:
                if(not isinstance(channel, Channel)):
                    raise Exception("add_channel_to_backups takes Channel type only")
                elif(channel in self.backuped_channels):
                    logging.getLogger().warn(f"Channel {channel.id} already in backuped_channels")
                else:
                    self.backuped_channels.append(channel)
            self.vars_manager.update_var("backuped_channels")
        except Exception as e:
            logging.getLogger().exception(str(e))

    def channel_backuped(self, channel_id : str):
        target_filename = f"{channel_id}.json"
        
        for root, dirs, files in os.walk(str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])):
            if target_filename in files:
                return True

        return False

    async def check_channels(self, ctx) -> list[discord.TextChannel]:
        not_found_channels = []

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                channel_id = str(channel.id)
                if not self.channel_backuped(channel_id):
                    not_found_channels.append(channel)

        return not_found_channels
    
    async def refresh_backuped_channels(self, ctx):
        await self.remove_all_channels()
        not_found_channels = await self.check_channels(ctx)
        for channel in not_found_channels:
            await self.try_add_backuped_channel(channel)
        logging.getLogger().info(f"Backup channels refreshed. New backuped channels: {[channel.name for channel in not_found_channels]}")

    async def try_add_backuped_id(self, id):
        try:
            id = int(id)
            discord_channel = await self.fetch_channel(id)
            added = await self.try_add_backuped_channel(discord_channel)
            if(not added):
                logging.getLogger().warn(f"Failed to add backuped id: {id}")
            return added
        except Exception as e:
            logging.getLogger().warn(f"Failed to fetch channel with backuped id: {id} {e}")
            return False

    async def try_add_backuped_channel(self, discord_channel):
        id = discord_channel.id
        if(self.check_if_id_present(id)):
            logging.info(f"Id already present {id}")
            return False
        if(isinstance(discord_channel,discord.CategoryChannel)):
            bot_category = Category(self, self.vars[VariableTypeEnum.BACKUP_PATH])
            bot_category.copy_from_category(discord_channel)
            self.backuped_categories.append(bot_category)
            self.update_backuped_var()
            return True
        elif(isinstance(discord_channel,discord.TextChannel)):
            bot_channel = Channel(self, self.vars[VariableTypeEnum.BACKUP_PATH])
            bot_channel.copy_from_channel(discord_channel)
            self.backuped_channels.append(bot_channel)
            self.update_backuped_var()
            return True
        elif(isinstance(discord_channel, Channel) or isinstance(discord_channel, Category)):
            raise Exception("try_add_backuped_channels inputs discord types")
        return False

    async def backup_channels(self):
        for category in self.backuped_categories:
            try:
                await category.backup()
            except Exception as e:
                logging.getLogger().error(f"Couldn't backup category {category.id} reason: {e}")
        for channel in self.backuped_channels:
            try:
                await channel.backup()
            except Exception as e:
                logging.getLogger().error(f"Couldn't backup channel {channel.id} reason: {e}")

