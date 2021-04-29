import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(
            title='**Roblox Narrator | Commands!**',
            description='Hello! This is Roblox Narrator! \n This bot is designed to interact with roblox! \n We have '
                        'range of commands from Games to Avatar Shop!',
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/836890659902193694/6a9800eefd79f16f116d9e1b428bb93b.png?size=128')

        embed.add_field(
            name='**Groups**',
            value='**>group_info {group-id}** -> This command will tell you basic information about the group! \n\n '
                  '**>search_groups {keyword}** -> This will get you 5 best results of your search! \n\n'
                  '**>search_members {group-id} {role-name}** -> You will get all members that are in specified role of group! \n\n'
                  '**>get_roles {group-id}** -> You will get list of all roles in group and their ID! \n\n',
            inline=False
        )
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(help(client))