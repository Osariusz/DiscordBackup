import discord
import asyncio

from collections import UserDict

class Reaction():
    
    async def copy_users(self, reaction : discord.Reaction):
        self.users = []

        users = await reaction.users().flatten()
        for user in users:
            self.users.append(user.id)


    async def copy_discord_reaction(self, reaction : discord.Reaction):
        await self.copy_users(reaction)

        self.emoji = str(reaction.emoji)

        self.__dict__.update()