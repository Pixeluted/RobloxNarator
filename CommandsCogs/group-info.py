import discord
from discord.ext import commands
from Utility.CommandUtilities import *
import json
import requests


class group_info(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def group_info(self,ctx, *, ID=None):
        print(ID)
        if ID == None:
            await send_error(ctx, 'You did not enter group ID!')
        else:
            convertedID = int(ID)

            groupinfo = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{convertedID}').text)
            print(groupinfo)

            if 'errors' in groupinfo:
                await send_error(ctx,"This group doesn't exist")
            else:
                embed = discord.Embed(
                    title=groupinfo["name"],
                    description=groupinfo["description"],
                    color=discord.Color.green()
                )

                embed.add_field(name='**Member Count**', value=groupinfo["memberCount"])
                embed.add_field(name='**Group Owner**', value=groupinfo["owner"]["username"])

                if not groupinfo["shout"] == None:
                    embed.add_field(name='**Group Shout**', value=groupinfo["shout"]["body"])

                embed.add_field(name="**Group Link**", value=f'https://www.roblox.com/groups/{convertedID}')

                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(group_info(client))