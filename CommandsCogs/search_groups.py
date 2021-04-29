import asyncio

import discord
from discord.ext import commands
from Utility.CommandUtilities import *
import json
import requests


class search_groups(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search_groups(self,ctx,*,keyword=None):
        if keyword == None:
            await send_error(ctx,'Please enter keyword!')
        else:
            proccesMessage = await send_notify_embed(ctx,'Searching...','Please give us a bit! We are searching!')

            searchResult = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&prioritizeExactMatch=true&limit=10').text)

            responseEmbed = discord.Embed(
                title=f'Search results for {keyword}',
                description='',
                color=discord.Color.green()
            )

            did = 1
            for groupNow in searchResult["data"]:
                if did <= 5:
                    moreGroupData = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{groupNow["id"]}').text)

                    responseEmbed.add_field(
                        name=f'{groupNow["name"]}',
                        value=f'**Member Count:** {groupNow["memberCount"]} \n **Owner:** {moreGroupData["owner"]["username"]} \n **Group ID:** {groupNow["id"]} \n [**Link**](https://www.roblox.com/groups/{groupNow["id"]})'
                    )
                    did += 1
            await asyncio.sleep(1)
            await proccesMessage.edit(embed=responseEmbed)
    @search_groups.error
    async def error(self,ctx,error):
        if isinstance(error,requests.HTTPError):
            await send_error(ctx,'There was problem with connecting to the servers! Please try again later!')
def setup(client):
    client.add_cog(search_groups(client))
