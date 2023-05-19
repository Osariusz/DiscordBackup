import discord
from Channel import Channel
from OwnerCog import OwnerCog
from discord.ext import commands
import asyncio
import os
import json
from Category import Category
import logging


class Bot(commands.Bot):

    def __init__(self,intents):
        super().__init__(command_prefix="$",intents=intents)
        self.backuped_channels = []
        self.backuped_categories = []
        self.vars = {}
        self.add_cog(OwnerCog(self))
        self.load_vars()

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

    def load_vars(self):
        required_vars = ["allowed_users","timezone"]
        for var in required_vars:
            var_path = os.path.join("vars",f"{var}.json")
            if(os.path.isfile(var_path)):
                with open(var_path,"r",encoding="utf-8") as file:
                    self.vars[var.replace(".json","")] = json.load(file)


    def check_if_id_present(self, id : int):
        result = self.get_backuped_channel(id)
        if(result == None):
            return False
        return True

    async def try_add_backuped_channel(self, discord_channel):
        id = discord_channel.id
        if(self.check_if_id_present(id)):
            return False
        if(isinstance(discord_channel,discord.CategoryChannel)):
            bot_category = Category(self)
            bot_category.copy_from_category(discord_channel)
            self.backuped_categories.append(bot_category)
            return True
        elif(isinstance(discord_channel,discord.TextChannel)):
            bot_channel = Channel(self)
            bot_channel.copy_from_channel(discord_channel)
            self.backuped_channels.append(bot_channel)
            return True
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

