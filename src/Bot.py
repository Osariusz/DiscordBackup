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


class Bot(commands.Bot):

    def __init__(self,intents):
        super().__init__(command_prefix="$",intents=intents)
        self.loaded_vars = False
        self.backuped_channels = []
        self.backuped_categories = []
        self.vars = {}
        self.add_cog(OwnerCog(self))

    async def on_ready(self):
        if(not self.loaded_vars):
            self.load_vars()
            self.loaded_vars = True

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
        if("backuped_channels" in self.vars):
            for channel_id in self.vars["backuped_channels"]:
                await self.try_add_backuped_id(channel_id)
        if("backuped_categories" in self.vars):
            for category_id in self.vars["backuped_categories"]:
                await self.try_add_backuped_id(category_id)

    def load_vars(self):
        required_vars = ["allowed_users","timezone"]
        for var in [file[0:file.find(".json")] for file in os.listdir("vars") if os.path.isfile(os.path.join("vars",file))]:
            var_path = os.path.join("vars",f"{var}.json")
            if(os.path.isfile(var_path)):
                with open(var_path,"r",encoding="utf-8") as file:
                    self.vars[var.replace(".json","")] = json.load(file)
        for required_var in required_vars:
            if(not required_var in self.vars):
                logging.getLogger().error(f"Var {required_var} not present in var dictionary!")
        asyncio.ensure_future(self.load_backuped_ids())
        logging.getLogger().info("Vars loaded")


    def update_backuped_var(self):
        self.vars["backuped_channels"] = [channel.id for channel in self.backuped_channels]
        self.vars["backuped_categories"] = [category.id for category in self.backuped_categories]
        self.update_var("backuped_channels")
        self.update_var("backuped_categories")

    def update_var(self, name : str):
        if(not name in self.vars):
            logging.getLogger().error(f"Can't update var {name} as it is not present in the dictionary!")
            return
        var_path = os.path.join("vars",f"{name}.json")
        if(os.path.isfile(var_path)):
            with open(var_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(self.vars[name]))

    def check_if_id_present(self, id : int):
        result = self.get_backuped_channel(id)
        if(result == None):
            return False
        return True

    async def try_add_backuped_id(self, id):
        try:
            id = int(id)
            discord_channel = await self.fetch_channel(id)
            added = await self.try_add_backuped_channel(discord_channel)
            if(not added):
                logging.getLogger().warn(f"Failed to add backuped id: {id}")
        except Exception as e:
            logging.getLogger().warn(f"Failed to fetch channel with backuped id: {id} {e}")

    async def try_add_backuped_channel(self, discord_channel):
        id = discord_channel.id
        if(self.check_if_id_present(id)):
            return False
        if(isinstance(discord_channel,discord.CategoryChannel)):
            bot_category = Category(self)
            bot_category.copy_from_category(discord_channel)
            self.backuped_categories.append(bot_category)
            self.update_backuped_var()
            return True
        elif(isinstance(discord_channel,discord.TextChannel)):
            bot_channel = Channel(self)
            bot_channel.copy_from_channel(discord_channel)
            self.backuped_channels.append(bot_channel)
            self.update_backuped_var()
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

