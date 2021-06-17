#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from discord.ext import commands
import discord
import config


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), **kwargs)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, exc))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        await bot.change_presence(activity=discord.Game("with feelings."))

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            await context.send("Missing Arguments.")
        elif isinstance(exception, commands.errors.MissingRole):
            await context.send("You do not have the required roles.")
        elif isinstance(exception, commands.CommandNotFound):
            await context.send("Command not found.")
        elif isinstance(exception, ValueError):
            await context.send("Invalid argument type.")
        else:
            raise exception


bot = Bot(intents=discord.Intents.all(), help_command=None)


## General Commands

#Display all commands
@bot.command()
async def helpme(ctx):
    ctx.send(embed=discord.Embed(title="tobeimplemented"))

#Get bot Ping
@bot.command(aliases=['Ping', 'Latency', 'latency'])
async def ping(ctx):
    await ctx.send(f"Ping {round(bot.latency * 1000)}ms")

#Reload Cog
@bot.command(hidden=True)
@commands.has_role("Admin")
async def reload_cog(ctx, name : str):
    try:
        bot.unload_extension(name)
        bot.load_extension(name)
    except Exception as e:
        await ctx.send(f"{e.message}")
    else:
        await ctx.send("Cod Reloaded!")

bot.run(config.token)
