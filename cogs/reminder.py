import discord
from discord.ext import commands
import asyncio

class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.requests = 0
    
    async def reminder(self, requestedBy, to, msg, time):
        embedvar = discord.Embed(title="Reminder!", description=msg)
        embedvar.set_footer(text=f"from {requestedBy}")

        await asyncio.sleep(time * 60 * 60)
        await to.send(embed=embedvar)

    @commands.has_role("Admin")
    @commands.command()
    async def remind(self, ctx, name):

        if name not in ctx.guild.members.name:
            ctx.send("Invalid name")
            return

        def check(m):
            if m.channel == discord.DMChannel and m.author.id == ctx.author.id:
                return True
            return False

        try:
            await ctx.author.send("Give me the message:")
            message = await self.client.wait_for('message', timeout = 60.0, check=check)
            await ctx.author.send("In how many many hours ? (0.01 to 48)")
            time = await self.client.wait_for('message', timeout = 60.0, check=check) 
            time = float(time)

            if time >= 0.01 and time <= 48: 
                asyncio.run(self.reminder(ctx.author.display_name, nessage, time))                                               
            else:
                ctx.author.send("Time out of range")
                return

        except asyncio.TimeoutError:
            await ctx.author.send("Timedout")
        except ValueError:
            await ctx.author.send("Invalid Time Input")




def setup(client):
    client.add_cog(Reminder(client))