import discord
from discord.ext import commands

from CONSTANTS import ROOM_CATEGORY_ID as ROOM_ID

class Roommaker(commands.Cog):

    def __init__(self, client):
        self.client = client

    ## Events
    # Creating member room on joining    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = await member.guild.create_text_channel(f'{member.display_name}')
        await channel.edit(category= discord.utils.get(member.guild.categories, id=ROOM_ID))

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