import asyncio
import os
import discord
from discord.ext import commands

prefix = '!'

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=prefix, intents=intents)

client.remove_command('help')

for filename in os.listdir('./CommandsCogs'):
    if filename.endswith('.py'):
        client.load_extension(f'CommandsCogs.{filename[:-3]}')
        print(f'Loading {filename}')
        print(f'Successfully loaded {filename}')

client.run('ODM2ODkwNjU5OTAyMTkzNjk0.YIklKQ.bt-r6mihkz69u9sn9LEafw1RJTE')
