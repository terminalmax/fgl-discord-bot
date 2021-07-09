import json
import random

import discord
from discord.ext import commands, tasks

from CONSTANTS import GENERAL_CHANNEL_ID

class PeriodicMessages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_channel = None
        self.count = 0

    # Commands
    @commands.command()
    async def strpm(self, ctx,arg=None):
        if arg == None:
            self.message_channel = ctx.channel
        else:
            self.message_channel = GENERAL_CHANNEL_ID
            
        self.periodicRandomMessage.start()
    
    @commands.command()
    async def stpm(self, ctx, arg=None):
        self.message_channel = ctx.channel
        self.periodicMessage.start()

    @commands.command()
    async def stoppm(self, ctx):
        self.periodicMessage.stop()

    @commands.command()
    async def stopprm(self, ctx):
        self.periodicRandomMessage.stop()

    # Tasks
    @tasks.loop(hours=8.0)
    async def periodicMessage(self):
        with open('Data/periodiclinks.json', 'r') as file:

            data = json.load(file)

            if self.count >= len(data['messages']):
                return

            message = data['messages'][self.count]
            self.count = self.count + 1

            print(message)
            await self.message_channel.send('@everyone ' + message)


    @tasks.loop(hours=8.0)
    async def periodicRandomMessage(self):
        with open('Data/periodiclinks.json', 'r') as file:
            data = json.load(file)
            
            message = data['messages'][random.randint(0,len(data['messages'])-1)]

            print(message)
            await self.message_channel.send('@everyone ' + message)
            

def setup(client):
    client.add_cog(PeriodicMessages(client))