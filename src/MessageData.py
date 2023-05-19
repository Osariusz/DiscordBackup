from Reaction import Reaction
import discord
import asyncio
from collections import UserDict
import Attachment
import datetime
from zoneinfo import ZoneInfo

class MessageData():

    async def add_reaction(self, reaction):
        new_reaction = Reaction()
        await new_reaction.copy_discord_reaction(reaction)
        self.reactions.append(new_reaction)

    def add_attachment(self, attachment_name):
        self.attachments.append(attachment_name)

    async def copy_message_attributes(self, message : discord.Message, timezone : str, thread_messages : list):
        self.id = message.id
        self.content = message.content
        self.author_id = message.author.id
        self.attachments = []
        self.reactions = []
        self.thread_messages = thread_messages
        for reaction in message.reactions:
            await self.add_reaction(reaction)

        messageReference = message.reference
        if(not messageReference == None):
            self.referenced_message = messageReference.message_id
            
        self.created_at = str(message.created_at.astimezone(ZoneInfo(timezone)))
        if(message.edited_at == None):
            self.edited_at = None
        else:
            self.edited_at = str(message.edited_at.astimezone(ZoneInfo(timezone)))

        self.pinned = message.pinned