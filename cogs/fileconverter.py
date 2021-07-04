import discord
from discord.ext import commands

class FileConverter(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Command()
	async def chess(self, ctx):
		

def setup(client):
	client.add_cog(FileConverter(client))