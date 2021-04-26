import json
from datetime import datetime
import pytz


import discord
from discord.ext import commands

class UsersTime(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    
    @commands.has_role("Admin")
    @commands.command()
    async def getTime(self, ctx):
        with open('Data/timezones.json', 'r') as read_file:
            zones = json.load(read_file)
            embedVar = discord.Embed(title='Time')
            for user_id in zones:
                try:
                    name = ctx.guild.get_member(int(user_id)).display_name
                    date = datetime.now(pytz.timezone(zones[user_id]))
                    embedVar.add_field(name=name, value=date.strftime("%Y/%m/%d %I:%M %p"), inline=False)
                except AttributeError:
                    continue
            await ctx.send(embed=embedVar)
            

    @commands.has_role("Admin")
    @commands.command()
    async def setMyTime(self, ctx):
        pass

def setup(client):
    client.add_cog(UsersTime(client))
