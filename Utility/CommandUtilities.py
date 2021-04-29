import discord
from discord.ext import commands,tasks

async def send_error(ctx,error):
    embed = discord.Embed(
        title='ERROR',
        description=error,
        color=discord.Color.red()
    )

    await ctx.send(embed=embed,delete_after=10)
async def send_permission_error(ctx):
    embed = discord.Embed(
        title='ERROR',
        description="You don't have permissions to use this command!",
        color=discord.Color.red()
    )

    await ctx.send(embed=embed,delete_after=10)
async def send_unexpected_error(ctx,error):
    embed = discord.Embed(
        title='UNEXPECTED ERROR',
        description=f'`{error}`',
        color=discord.Color.red()
    )

    await ctx.send(embed=embed,delete_after=10)
async def send_notify_embed(ctx,title,description,delete=None,after=None):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.blue()
    )

    if delete == False or delete == None:
        return await ctx.send(embed=embed)
    else:
        return await ctx.send(embed=embed,delete_after=after)
async def send_sucesfull_embed(ctx,title,description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.green()
    )

    await ctx.send(embed=embed)