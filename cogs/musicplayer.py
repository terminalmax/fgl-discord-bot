import json

import discord
from discord.ext import commands
from discord.utils import get

class MusicPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mqueue = []
        self.is_playing = False
        self.is_connected = False
        self.favlist = None

        #with open("Data/favouritemusic.json", "r") as mlist:
        #    favlist = json.load(mlist)

    @commands.has_role("Admin")
    @commands.command():
    async def play(self, ctx, mlink):
        pass


    @commands.has_role("Admin")
    @commands.command()
    async def pause(self, ctx):
        pass
        
    
    @commands.has_role("Admin")
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.sent("Not in any VC!")


def setup(client):
    client.add_cog(MusicPlayer(client))
    