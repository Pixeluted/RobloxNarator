import discord
from discord.ext import commands
from Utility.CommandUtilities import *
import json
import requests


class on_guild_join(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self,guild):

        with open('../database.json') as file:
            loadedFile = json.load(file)

        isInList = False

        for checkingGuild in loadedFile["guilds"]:
            print(checkingGuild)
            if int(checkingGuild["guild-id"]) == guild.id:
                isInList = True
                break

        if isInList == True:
            print('This guild is already in list!')
        else:
            loadedFile["guilds"].append({
                "guild-id": guild.id,
                "global-group-id": None,
                "users": [

                ]
            })

            with open('../database.json', 'w') as f:
                json.dump(loadedFile, f, indent=4)
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot has started!')
def setup(client):
    client.add_cog(on_guild_join(client))