import discord
import os
from Message import Message
import json
import asyncio
from CustomEncoder import CustomEncoder
import datetime
import logging

class Channel():

    def __init__(self, bot, backups_path: str):
        self.messages: list[Message] = []
        self.bot = bot
        self.server_id = 0
        self.backups_path = backups_path

    async def get_channel_messages(self):
        # TODO: Add limiting messages to after the last start date
        self.messages = []
        max_python_array_size = 536870912
        messages = await self.channel.history(limit=max_python_array_size).flatten()
        messages.reverse()
        for discord_message in messages:
            bot_message = Message(self.bot)
            await bot_message.copy_from_message(discord_message)
            self.messages.append(bot_message)
        logging.getLogger().info(f"Got {len(self.messages)} messages in {self.id}")

    def copy_from_channel(self, channel : discord.TextChannel):
        self.channel = channel
        self.id = channel.id
        self.name = channel.name
        self.server_id = channel.guild.id

    async def send_all_messages(self, channel : discord.TextChannel):
        for message in self.messages:
            await channel.send(f"{message.message_data.created_at} {message.message_data.author_id}: {message.message_data.content}")

    def add_message(self, message : Message):
        self.messages.append(message)

    def load_messages(self, json_str : str):
        message_datas = json.loads(json_str)
        for message_data in message_datas:
            message = Message(self.bot)
            message.load_message_data(json.dumps(message_data))
            self.add_message(message)

    async def backup(self, category_path=""):
        logging.getLogger().info(f"Backuping channel {self.id}")
        start_time = datetime.datetime.now()
        await self.get_channel_messages()

        if(not os.path.exists(self.channel_folder(category_path=category_path))):
            os.makedirs(str(self.channel_folder(category_path=category_path)))


        for message in self.messages:
            if(len(message.attachments)>0):
                if(not os.path.exists(self.attachments_folder(category_path))):
                    os.makedirs(self.attachments_folder(category_path))
                await message.backup_attachments(self.attachments_folder(category_path))

        with open(self.channel_file(category_path),"w", encoding="utf-8") as file:
            file.write(json.dumps(self.messages,cls=CustomEncoder, ensure_ascii=False))

        end_time = datetime.datetime.now()
        logging.getLogger().info(f"Backuped channel {self.id} in {end_time-start_time}")

    def channel_folder(self,category_path=""):
        return os.path.join(self.backups_path,f"{self.server_id}",f"{category_path}",f"{self.id}")

    def channel_file(self ,category_path=""):
        return os.path.join(self.channel_folder(category_path=category_path),f"{self.id}.json")

    def attachments_folder(self,category_path=""):
        return os.path.join(self.channel_folder(category_path=category_path),"attachments")