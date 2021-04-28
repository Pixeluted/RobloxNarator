import discord
from discord.ext import commands,tasks
import requests
import json

prefix = '!'

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=prefix, intents=intents)

client.remove_command('help')

# Utility Functions

async def send_error(ctx,error):
    embed = discord.Embed(
        title='ERROR',
        description=error,
        color=discord.Color.red()
    )

    await ctx.send(embed=embed)
async def send_permission_error(ctx):
    embed = discord.Embed(
        title='ERROR',
        description="You don't have permissions to use this command!",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed)
async def send_unexpected_error(ctx,error):
    embed = discord.Embed(
        title='UNEXPECTED ERROR',
        description=f'`{error}`',
        color=discord.Color.red()
    )

    await ctx.send(embed=embed)

# Bot Commands
@client.command()
async def help(ctx):
    embed = discord.Embed(
        title='Bot Commands',
        description='Roblox Narrator is an discord bot that is interacting with roblox! You can use this as global (not-logged-in) or as local (you use roblox token to login!)! \n **WE ARE NOT SAVING ANY ROBLOX TOKENS**',
        color=discord.Color.blue()
    )

    embed.add_field(name='**Global Use**',value='!group-info {group-id} - This will return information about the specific group! \n \n !member-count - This will get member count of the global group set!',inline=False)
    embed.add_field(name='**Configuration**',value='!set-group-id {group-id} - This will set your globally choosed group for  this guild! Only admins can use this command!',inline=False)

    await ctx.send(embed=embed)
@client.command(name='group-info')
async def group_info(ctx,*,ID=None):
    print(ID)
    if ID == None:
        await send_error(ctx,'You did not enter group ID!')
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

            embed.add_field(name='**Member Count**',value=groupinfo["memberCount"])
            embed.add_field(name='**Group Owner**',value=groupinfo["owner"]["username"])

            if not groupinfo["shout"] == None:
                embed.add_field(name='**Group Shout**', value=groupinfo["shout"]["body"])

            embed.add_field(name="**Group Link**",value=f'https://www.roblox.com/groups/{convertedID}')

            await ctx.send(embed=embed)
@client.command(name='set-group-id')
@commands.has_permissions(manage_guild=True)
async def set_group_id(ctx,*,ID=None):
    if ID == None:
        await send_error(ctx,'You did not enter group ID!')
    else:
        with open('database.json') as file:
            loadedFile = json.load(file)

        for checkingGuild in loadedFile["guilds"]:
            if int(checkingGuild["guild-id"]) == ctx.guild.id:
                guild = checkingGuild
                break

        guild["global-group-id"] = int(ID)

        with open('database.json','w') as f:
            json.dump(loadedFile,f, indent=4)

        embed = discord.Embed(
            title='Successfully changed!',
            description=f'Global group id was changed to {ID} for {ctx.guild.name}!',
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)
@client.command(name='member-count')
async def member_count(ctx):
  with open('database.json') as file:
            loadedFile = json.load(file)
  for checkingGuild in loadedFile["guilds"]:
            if int(checkingGuild["guild-id"]) == ctx.guild.id:
                guild = checkingGuild
                break
  if guild["global-group-id"] == None:
    await send_error(ctx,'Please set global group id! !set-group-id {group-id}')
  else:
    groupinfo = json.loads(requests.get(f'https://groups.roblox.com/v1/groups/{guild["global-group-id"]}').text)

    embed = discord.Embed(
      title=f'{groupinfo["name"]} Member Count!',
      description=f'{groupinfo["name"]} has {groupinfo["memberCount"]} members!',
      color=discord.Colour.green()
    )

    await ctx.send(embed=embed)

# Commands Error
@set_group_id.error
async def set_group_id_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await send_permission_error(ctx)
    else:
        await send_unexpected_error(ctx,error)
# Bot Events
@client.event
async def on_guild_join(guild):

    with open('database.json') as file:
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

        with open('database.json', 'w') as f:
            json.dump(loadedFile, f, indent=4)
@client.event
async def on_ready():
  print('Bot has started!')

client.run('ODM2ODkwNjU5OTAyMTkzNjk0.YIklKQ.bt-r6mihkz69u9sn9LEafw1RJTE')
