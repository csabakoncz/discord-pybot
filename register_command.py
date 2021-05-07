import aiohttp
import asyncio
import json as JSON
import logging
import os

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.getenv('DISCORD_TOKEN')


async def print_response(response):
    print("Status:", response.status)
    html = await response.text()
    print("Body:", html)
    return html


async def get(session: aiohttp.ClientSession, path=''):
    return await req(session, method='GET', path=path)


async def post(session: aiohttp.ClientSession, path='', json=None):
    return await req(session, method='POST', path=path, json=json)


async def req(session: aiohttp.ClientSession, method='GET', path='', json=None):
    url = 'https://discord.com/api/v8/'+path
    headers = {"Authorization": "Bot "+TOKEN}

    request_context = session.request(
        method=method, url=url, headers=headers, json=json)

    async with request_context as response:
        response_text = await response.text()
        return JSON.loads(response_text)


async def main():

    async with aiohttp.ClientSession() as session:
        app_data = await get(session, '/oauth2/applications/@me')
        app_name = app_data['name']

        guilds = await get(session, '/users/@me/guilds')

        for g in guilds:
            commands_path = '/applications/%s/guilds/%s/commands' % (
                app_data['id'], g['id'])

            await create_greeter(session, app_name, commands_path)
            await create_foci_ma(session, app_name, commands_path)

            commands = await get(session, commands_path)
            print('all commands in this guild = %s' %
                  JSON.dumps(commands, indent=2))


async def create_greeter(session, app_name, commands_path):
    data = {
        "name": app_name+"-greet",
        "description": "Greets you",
        "options": [
            {
                "type": 3,
                "name": "name",
                "description": "Your name",
                "required": True
            },
            {
                "type": 4,
                "name": "age",
                "description": "Your age"
            }
        ]
    }

    command = await post(session, path=commands_path, json=data)
    print('command created = %s' % JSON.dumps(command, indent=2))

async def create_foci_ma(session, app_name, commands_path):
    data = {
        "name": app_name+"-foci-ma",
        "description": "Todays football matches"
    }

    command = await post(session, path=commands_path, json=data)
    print('command created = %s' % JSON.dumps(command, indent=2))

asyncio.run(main(), debug=False)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
