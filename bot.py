# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('MTEwMzcwMTk4NDQ3OTAyMzE0NQ.G4wBJu.YMSkSVcgycrZ4UGQxLEDSFWjXkx2p-ulnyIhSY')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
