# bot.py
import os
import sys

import discord
from dotenv import load_dotenv
import hupper

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

    print('message received: %s'%message.content)
    print('message channel=%s'%message.channel)
    print('message author is %s'%message.author.display_name)

    if message.content.lower() == 'ping':
        await message.channel.send('Pong!')

def main(args=sys.argv[1:]):
    if '--reload' in args:
        # start_reloader will only return in a monitored subprocess
        hupper.start_reloader('bot.main')

    client.run(TOKEN)

if __name__ == '__main__':
    main()
