import json
from datetime import datetime
import pytz
import asyncio
import itertools

import discord
from discord.ext import commands

from CONSTANTS import ALL_TIME_ZONES
from CONSTANTS import YES_EMOJI, NO_EMOJI, CANCEL_EMOJI
class UsersTime(commands.Cog):
    

    def __init__(self, client):
        self.client = client
        self.MESSAGE_LINK = None


    #Displaying all timezones
    @commands.has_role("Admin")
    @commands.command()
    async def get_timezone_list(self, ctx):
        await ctx.message.delete()

        for tzone in ALL_TIME_ZONES:
            messagestr = ""
            for index, zone in enumerate(ALL_TIME_ZONES[tzone]):
                messagestr = messagestr + f"    {index}:{zone}\n"
                

            newembed = discord.Embed(title=tzone, description = messagestr, color=0xFFFFF0)
            newembed.set_footer(text="Set time zone with $setMyTime <ZONE> <NUMBER>")
            await ctx.send(embed=newembed)
            messagestr = ""


    @commands.has_role("Admin")
    @commands.command()
    async def set_list_link(self, ctx, link):
        self.MESSAGE_LINK = link
        await ctx.send("Link Set!")

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
    
    # To set user time
    @commands.has_role("Admin")
    @commands.command()
    async def setMyTime(self, ctx, selected_zone = None, selected_number = None):

        if selected_zone == None:
            await ctx.send(f'{self.MESSAGE_LINK}')
            await ctx.send("Use '$setMyTime <ZONE> <NUMBER>' to set your timezone!")
        elif selected_number == None:
            await ctx.send("Missing Argument")
            await ctx.send("Use '$setMyTime <ZONE> <NUMBER>' to set your timezone!")
        else:
            zones = None
            try:
                with open("Data/timezones.json", 'r') as file:
                    file.seek(0)
                    zones = json.load(file)
                    zones[str(ctx.author.id)] = ALL_TIME_ZONES[selected_zone][int(selected_number)]
                with open("Data/timezones.json", 'w') as file:
                    file.seek(0)
                    json.dump(zones, file)
                    await ctx.send("timezone set!")
            except IndexError:
                await ctx.send("Index Error!")
                
    #To hold quick votes
    @commands.has_role("Admin")
    @commands.command()
    async def quickvote(self, ctx, voteTitle, duration):
        
        await ctx.message.delete()
        
        try:
            duration = float(duration)
            if  duration > 60 or duration < 1:
                await ctx.send("Invalid time!")
                return
        except:
            await ctx.send("Invalid Argument(s)!")
            return

        newembed = discord.Embed(title= f'{voteTitle}')
        newembed.add_field(name= "\u200b", value=f"Agree with {YES_EMOJI}", inline = False)
        newembed.add_field(name= "\u200b" ,value=f"Disagree with {NO_EMOJI}", inline = False)
        newembed.add_field(name= "\u200b", value=f"Cancel with {CANCEL_EMOJI}", inline = False)
        newembed.set_footer(text=f"Requested by @{ctx.author.name} for {duration}mins.")
        message = await ctx.send(embed=newembed)
        await message.add_reaction(YES_EMOJI)
        await message.add_reaction(NO_EMOJI)
        await message.add_reaction(CANCEL_EMOJI)

        agreeList = []
        disagreeList = []
        whocancel = ""

        def check1(reaction, user):
            if reaction.message == message and not user.bot:
                try:
                    if f'<:{reaction.emoji.name}:{reaction.emoji.id}>' == CANCEL_EMOJI:
                        nonlocal whocancel
                        whocancel = user.display_name
                        return True
                    elif f'<:{reaction.emoji.name}:{reaction.emoji.id}>' == YES_EMOJI:
                        if user.display_name not in agreeList:
                            agreeList.append(user.display_name)
                    elif f'<:{reaction.emoji.name}:{reaction.emoji.id}>' == NO_EMOJI:
                        if user.display_name not in disagreeList:
                            disagreeList.append(user.display_name)
                except AttributeError:
                    pass
            return False
        
        def check2(reaction, user):
            if reaction.message == message and not user.bot:
                try:
                    if f'<:{reaction.emoji.name}:{reaction.emoji.id}>' == YES_EMOJI:
                        if user.display_name in agreeList:
                            agreeList.remove(user.display_name)
                    elif f'<:{reaction.emoji.name}:{reaction.emoji.id}>' == NO_EMOJI:
                        if user.display_name in disagreeList:
                            disagreeList.remove(user.display_name)
                except AttributeError:
                    pass
                return False
        
        done, pending = await asyncio.wait([
            self.client.wait_for('reaction_add', check = check1, timeout = duration*60),
            self.client.wait_for('reaction_remove', check= check2)], 
            return_when = asyncio.FIRST_COMPLETED)

        try:
            stuff = done.pop().result()
        except asyncio.TimeoutError:
            agreestring = ' '.join(agreeList)
            disagreestring = ' '.join(disagreeList)

            newembed = discord.Embed(title= f'{voteTitle}', color=0x00FF00)
            newembed.add_field(name="Agreed by:", value=f'>{agreestring}', inline = False)
            newembed.add_field(name="Disagreed by:", value=f'>{disagreestring}', inline = False)
            newembed.set_footer(text=f"Requested by {ctx.author.display_name} for {duration}mins.")
            await ctx.send(embed=newembed)
            await message.delete()
        else:
            cancel = discord.Embed(title=f"{voteTitle}", description=f"Terminated by {whocancel}", color = 0xFF0000)
            cancel.set_footer(text=f"Requested by {ctx.author.display_name} for {duration}mins.")
            await ctx.send(embed=cancel)
            await message.delete()
        
        for future in done:
            future.exception()

        for future in pending:
            future.cancel()


    
    @commands.has_role("Admin")
    @commands.command()
    async def change_yes_emoji(self, ctx, new_emoji):
        YES_EMOJI = new_emoji
        await ctx.send("Changed!")


    @commands.has_role("Admin")
    @commands.command()
    async def change_no_emoji(self, ctx, new_emoji):   
        NO_EMOJI = new_emoji
        await ctx.send("Changed!")


    @commands.has_role("Admin")
    @commands.command()
    async def change_cancel_emoji(self, ctx, new_emoji):
        CANCEL_EMOJI = new_emoji
        await ctx.send("Changed!")


def setup(client):
    client.add_cog(UsersTime(client))
