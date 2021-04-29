import discord
from discord.ext import commands
import requests
import json
from Utility.CommandUtilities import *

class member_count(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def member_count(self,ctx):
        with open('database.json') as file:
            loadedFile = json.load(file)
        for checkingGuild in loadedFile["guilds"]:
            if int(checkingGuild["guild-id"]) == ctx.guild.id:
                guild = checkingGuild
                break
        if guild["global-group-id"] == None:
            await send_error(ctx, 'Please set global group id! !set-group-id {group-id}')
        else:
            groupinfo = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{guild["global-group-id"]}').text)

            embed = discord.Embed(
                title=f'{groupinfo["name"]} Member Count!',
                description=f'{groupinfo["name"]} has {groupinfo["memberCount"]} members!',
                color=discord.Colour.green()
            )

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(member_count(client))