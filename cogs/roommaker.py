import json

import discord
from discord.ext import commands

from CONSTANTS import ROOM_CATEGORY_ID as ROOM_ID
from CONSTANTS import BOT_STATUS_CHANNEL_ID as STATUS_ID

class Roommaker(commands.Cog):

    def __init__(self, client):
        self.client = client

    ## Events
    # Creating member room on joining    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        with open('Data/timezones.json', 'r') as read_file:
            rooms = json.load(read_file)
            
            if member.id not in rooms:
                channel = await member.guild.create_text_channel(f'{member.display_name}')
                await channel.edit(category= discord.utils.get(member.guild.categories, id=ROOM_ID))
                await discord.utils.get(ctx.guild.channels, id=STATUS_ID).send(f"Made room for {member.display_name}")
    
    @commands.Cog.listener()
    async def on_member_leave(self, member):
        pass

    ## Commands
    # Getting member room link
    @commands.has_role("Admin")
    @commands.command()
    async def myroom(self, ctx):
        await ctx.send(" ")

    # Making room with name
    @commands.has_role("Admin")
    @commands.command()
    async def makeroom(self, ctx, name):
        channel = await ctx.guild.create_text_channel(f'{name}')
        await channel.edit(category=discord.utils.get(ctx.guild.categories, id=ROOM_ID))


def setup(client):
    client.add_cog(Roommaker(client))