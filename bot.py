# bot.py
import eliza
import hupper
from dotenv import load_dotenv
from discord.ext import commands
from discord.http import HTTPClient, Route
from discord.message import Message
from discord.state import ConnectionState
import discord
import os
import sys
import logging

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL')
if LOG_LEVEL and hasattr(logging, LOG_LEVEL):
    log_level = getattr(logging, LOG_LEVEL)
else:
    log_level = logging.INFO
print('LOG_LEVEL is %s' % LOG_LEVEL)
print('log_level is %s' % log_level)

logging.basicConfig(level=log_level)
log = logging.getLogger('bot.py')
log.info('info level works')

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True


class Interaction:
    def __init__(self, channel, data, state):
        self.channel = channel
        self.data = data
        self.state = state


class MyConnectionState(ConnectionState):
    def parse_interaction_create(self, data):
        channel, _ = self._get_guild_channel(data)
        i = Interaction(channel=channel, data=data, state=self)
        self.dispatch('interaction', i)


class MyBot(commands.Bot):
    def _get_state(self, **options):
        return MyConnectionState(dispatch=self.dispatch, handlers=self._handlers,
                                 hooks=self._hooks, syncer=self._syncer, http=self.http, loop=self.loop, **options)


bot = MyBot(command_prefix='/', description='unsmart bot', intents=intents)
# bot = commands.Bot(command_prefix='/', description='unsmart bot', intents=intents)
# client = discord.Client()
client = bot

therapists = {}


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


def get_command_option(command_data, name):
    opts = [opt for opt in command_data['options'] if opt['name'] == name]
    if opts:
        return opts[0]['value']


@client.event
async def on_interaction(i: Interaction):
    log.info('interaction channel=%s', i.channel)
    # log.info('interaction data is %s', i.data)
    iid = i.data['id']
    itoken = i.data['token']

    msg = 'What?'
    greet_command = '%s-greet' % client.user.name.lower()

    command_data = i.data['data']

    if command_data['name'] == greet_command:
        greetee = get_command_option(command_data, 'name')
        age = get_command_option(command_data, 'age')

        if age is not None:
            greetee += ' (%s)' % age

        msg = 'Hello, %s!' % greetee

    payload = {
        'type': 4,
        'data': {
            'content': msg
        }
    }

    http_client: HTTPClient = i.state.http
    route = Route('POST', '/interactions/%s/%s/callback' % (iid, itoken))
    await http_client.request(route, json=payload)


@client.event
async def on_message(message: discord.message.Message):
    if message.author == client.user:
        return

    log.info('message received: %s', message.content)
    log.info('message channel=%s', message.channel)
    log.info('message author is %s', message.author.display_name)

    if message.content.lower() == 'ping':
        await message.channel.send('Pong!')

    other = message.author.display_name

    therapist = therapists.get(other)
    if therapist:
        await message.reply(therapist.respond(message.content))
        if message.content == 'quit':
            del therapists[other]
    elif message.content == 'Eliza?':
        therapist = eliza.eliza()
        therapists[other] = therapist
        await message.reply("Hello.  How are you feeling today?")


def main(args=sys.argv[1:]):
    if '--reload' in args:
        # start_reloader will only return in a monitored subprocess
        hupper.start_reloader('bot.main')

    client.run(TOKEN)


if __name__ == '__main__':
    main()
