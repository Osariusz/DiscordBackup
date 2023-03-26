import discord
from MessageData import MessageData
import json
from Attachment import Attachment

class Message():

    def __init__(self, bot : discord.Client):
        self.bot = bot

    async def copy_from_message(self, message : discord.Message):
        self.message = message
        self.attachments = message.attachments
        self.message_data = MessageData()
        await self.message_data.copy_message_attributes(message, self.bot.vars["timezone"])

    def load_message_data(self, json_str):
        self.message_data = json.loads(json_str,object_hook=lambda d: MessageData(**d))

    async def backup_attachments(self, channel_attachments_path):
        for discord_attachment in self.attachments:
            attachment = Attachment(self.bot)
            attachment.copy_from_attachment(discord_attachment)
            new_name = await attachment.save_to_free_name(channel_attachments_path)
            self.message_data.add_attachment(new_name)

    async def send_to_discord(self):
        channel = await self.bot.fetch_channel(696979620888576060)
        await channel.send(self.message_data.content)
