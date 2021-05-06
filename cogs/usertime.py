import json
from datetime import datetime
import pytz
import asyncio

import discord
from discord.ext import commands

class UsersTime(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    
    @commands.has_role("Admin")
    @commands.command()
    async def getTime(self, ctx, user_name=None):
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
    async def setMyTime(self, ctx, selected_zone=None):

        if selected_zone == None:
            ctx.author.send(f"{pytz.all_timezones}")
            ctx.author.send("Use '$setMyTime number_from_list' to set your timezone!")
        else:
            with open("Data/timezones.json", 'r+') as file:
                file.seek(0);
                zones = json.load(file)
                zones[ctx.author.id] = pytz.all_timezones[selected_zone]
            #FINISH THIS PART

    @commands.has_role("Admin")
    @commands.command()
    async def quicksched(self, ctx, type):

        def check_message(m):
            if m.author.id == ctx.author.id and m.channel == discord.DMChannel():
                return True

        try:
            await ctx.author.send("Give me the title(50 words):")
            title = await self.client.wait_for("message", check= check_message, timeout=20)
            await ctx.author.send("Give me the description(200 words):")
            description = await self.client.wait_for("message", check=check_message, timeout=60)

            self.client.guild[0].get_channel

        except asyncio.TimeoutError:
            await ctx.author.send("Too Slow ! ! ! !")

def setup(client):
    client.add_cog(UsersTime(client))
