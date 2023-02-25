import discord
from discord.ext import commands

@commands.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong")