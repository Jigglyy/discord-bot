import os
import sys
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from commands import example_command
from data import database
from data import data_handler
import discord
from discord.ext import commands
import sqlite3
from loguru import logger
import datetime

# Setting up varibles

config = data_handler.read_file("config.json")
token = config['token']
prefix = config['prefix']
description = config['description']

# Call create_table to create the users table
database.create_table()

# Setup Handler for logs

class DiscordHandler(logging.Handler):
    def emit(self, record):
        logger.remove()
        today = datetime.date.today().strftime("%Y-%m-%d")
        log_filename = f"file_{today}.log"
        format = "<red>{level}</red> || <green>{time:DD-MM-YYYY HH:mm:ss}</green> || <level><yellow>{module}>{file}</yellow></level> || <blue>{message}</blue>"
        logger.add(logging.StreamHandler(sys.stderr), colorize=True, format=format)
        logger.add(log_filename,  level="DEBUG", rotation="10 MB", format=format)
        logger.opt(depth=6, exception=record.exc_info).log(record.levelno, record.getMessage())

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents, description=description)
handler = DiscordHandler()
handler.setLevel(logging.DEBUG)

# Commands

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    
@commands.command()
async def ping(ctx):
    logger.info("Heard Ping, sending Pong")
    await ctx.send("Pong")
bot.add_command(ping)

# Run Bot

bot.run(token, log_handler=handler)