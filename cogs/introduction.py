import discord
from discord.ext import commands

data

class Introduction(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready():
		

	@commands.command()
	async def introduce(self, ctx):


def setup(client):
	client.add_cog(Introduction(client))