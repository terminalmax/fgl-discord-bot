import json
import random

import discord
from discord.ext import commands, tasks

class PeriodicMessages(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def setPeriodicMessageChannel(self, ctx):
        pass
    
    @commands.command()
    async def startPeriodicMessages(self, ctx):
        self.periodicMessage.start()
    
    # Tasks
    @tasks.loop(hours=6.0)
    async def periodicMessage(self):
        with open('Data/periodiclinks.json', 'r') as file:
            data = json.load(file)
            
            link = data['links'][random.randint(0,(len(data['links']) - 1))]
            message = data['messages'][random.randint(0,len(data['messages'] - 1))]



def setup(client):
    client.add_cog(PeriodicMessages(client))