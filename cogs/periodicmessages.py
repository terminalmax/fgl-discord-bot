import json
import random

import discord
from discord.ext import commands, tasks

from CONSTANTS import GENERAL_CHANNEL_ID

class PeriodicMessages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_channel = None

    # Commands
    @commands.command()
    async def startPeriodicMessages(self, ctx, arg=None):
        await ctx.send("Starting Periodic Messages . . . . ")
        if arg == None:
            self.message_channel = ctx.channel
        else:
            self.message_channel = GENERAL_CHANNEL_ID
            
        self.periodicMessage.start()
    
    @commands.command()
    async def stopPeriodicMessages(self, ctx):
        self.periodicMessage.stop()

    # Tasks
    @tasks.loop(hours=1.0)
    async def periodicMessage(self):
        with open('Data/periodiclinks.json', 'r') as file:
            data = json.load(file)
            
            message = data['messages'][random.randint(0,len(data['messages'])-1)]

            print(message)
            await self.message_channel.send('@everyone ' + message)
            

def setup(client):
    client.add_cog(PeriodicMessages(client))