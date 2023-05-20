# This example requires the 'message_content' intent.
import os
import discord
from discord.ext import commands
from discord.utils import get
from pytube import YouTube
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import asyncio
#import youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = '!',intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Manager personal'))
    print('Estoy Vivoooo')


bot.run(TOKEN)