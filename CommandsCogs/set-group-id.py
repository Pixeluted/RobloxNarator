import discord
from discord.ext import commands

from RobloxNarator import client
from Utility.CommandUtilities import *
from Utility.GroupUtilities import *
import json
import asyncio

class set_group_id(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name='set-group-id')
    @commands.has_permissions(manage_guild=True)
    async def set_group_id(self,ctx, *, ID=None):
        if ID == None or str(ID).lower() == "none":
            notifyEmbed = await send_notify_embed(ctx, 'Confirm Prompt',
                                                  'Do you agree that you want to reset global group-id? Say `Yes` to confirm or `No` to cancel!')

            def input_check(msg):
                return msg.author == ctx.message.author and msg.channel == ctx.message.channel

            try:
                response = await client.wait_for("message", check=input_check, timeout=60)

                if response.content == "Yes":
                    with open('../database.json') as file:
                        loadedFile = json.load(file)
                    for checkingGuild in loadedFile["guilds"]:
                        if int(checkingGuild["guild-id"]) == ctx.guild.id:
                            guild = checkingGuild
                            break
                    guild["global-group-id"] = None

                    with open('../database.json', 'w') as f:
                        json.dump(loadedFile, f, indent=4)

                    await send_sucesfull_embed(ctx, 'Success!', 'Successfully resseted your global group-id!')
                elif response.content == "No":
                    await send_notify_embed(ctx, 'Prompt Cancelled!', 'This prompt has been cancelled!', True, 10)
                else:
                    await send_error(ctx, 'Invalid response! Cancelling this prompt!')
                    await asyncio.sleep(10)
                    await notifyEmbed.delete()

            except asyncio.TimeoutError:
                await send_error(ctx, 'The prompt has timed out!')
                await asyncio.sleep(10)
                await notifyEmbed.delete()
        else:
            if isThisGroupValid(ID):
                promptEmbed = await send_notify_embed(ctx, 'Confirm Prompt',
                                                      f'Do you want to be {getGroupName(ID)} your global group? Say `Yes` to confirm or `No` to cancel!')

                def input_check(msg):
                    return msg.author == ctx.message.author and msg.channel == ctx.message.channel

                try:
                    response = await client.wait_for("message", check=input_check, timeout=60)

                    if response.content == "Yes":
                        with open('database.json') as file:
                            loadedFile = json.load(file)
                        for checkingGuild in loadedFile["guilds"]:
                            if int(checkingGuild["guild-id"]) == ctx.guild.id:
                                guild = checkingGuild
                                break
                        guild["global-group-id"] = int(ID)

                        with open('database.json', 'w') as f:
                            json.dump(loadedFile, f, indent=4)

                        await send_sucesfull_embed(ctx, 'Success!', f'Successfully set your global group-id to {ID}!')
                    elif response.content == "No":
                        await send_notify_embed(ctx, 'Prompt Cancelled!', 'This prompt has been cancelled!', True, 10)
                    else:
                        await send_error(ctx, 'Invalid response! Cancelling this prompt!')
                        await asyncio.sleep(10)
                        await promptEmbed.delete()

                except asyncio.TimeoutError:
                    await send_error(ctx, 'The prompt has timed out!')
                    await asyncio.sleep(10)
                    await promptEmbed.delete()
            else:
                await send_error(ctx, "This group isn't valid or doesn't exist!")

    @set_group_id.error
    async def set_group_id_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await send_permission_error(ctx)
        else:
            await send_unexpected_error(ctx, error)


def setup(client):
    client.add_cog(set_group_id(client))