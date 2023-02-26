import os
import sys
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data import database
from data import data_handler
import discord
from discord.ext import commands
from loguru import logger
import datetime
import uuid
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from discord.errors import ConnectionClosed

# Setting up varibles

config = data_handler.read_file("config.json")
token = config['token']
prefix = config['prefix']
description = config['description']
bot_id = config['bot_id']

# Call create_table to create the users table

database.create_table()

# Setup Handler for logs

class DiscordHandler(logging.Handler):
    def emit(self, record):
        logger.remove()
        today = datetime.date.today().strftime("%Y-%m-%d")
        log_filename = f"bot_{today}.log"
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

@bot.event
async def on_message(msg):
    try:
        channel = msg.channel
        uuid_gen = str(uuid.uuid4())
        today = datetime.date.today().strftime("%Y-%m-%d")
        image_name = f"{today}_{uuid_gen}.png"
        await msg.attachments[0].save(image_name)
        
        try:
            img_a = Image.open("image.jpg")
            img_b = Image.open(image_name)
            img_diff = Image.new("RGBA", img_a.size)

            mismatch = pixelmatch(img_a, img_b, img_diff, includeAA=True)
            logger.info(mismatch)

            img_diff.save("diff.png")
            
            if mismatch > 300_000:
                await msg.delete()
                await channel.send(f"Your picture contains foul imagery, it has been deleted!")
                
        except ValueError as e:
            logger.error(str(e))
        

    except IndexError:
        if msg.author.id == bot_id:
            logger.info("Detected bot message in channel: " + str(msg.channel.name) + ", ignoring")
        else:
            logger.error("Index Error: No Attachments")


# Add Commands

bot.add_command(ping)

# Run Bot
try:
    bot.run(token, log_handler=handler)
except ConnectionClosed as e:
    logger.error(str(e))