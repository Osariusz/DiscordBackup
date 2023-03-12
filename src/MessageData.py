from Reaction import Reaction
import discord
import asyncio
from collections import UserDict

class MessageData():

    async def add_reaction(self, reaction):
        new_reaction = Reaction()
        await new_reaction.copy_discord_reaction(reaction)
        self.reactions.append(new_reaction)

    async def copy_message_attributes(self, message : discord.Message):
        self.id = message.id
        self.content = message.content
        self.author_id = message.author.id
        self.attachments = []
        self.reactions = []
        for reaction in message.reactions:
            await self.add_reaction(reaction)
            
        self.created_at = str(message.created_at)
        self.edited_at = str(message.edited_at)
        if(message.edited_at == None):
            self.edited_at = None
        self.pinned = message.pinned