# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: discord.message.Message):
    if message.author == client.user:
        return

    if message.content.lower() == 'ping':
        await message.channel.send('Pong!')

client.run(TOKEN)