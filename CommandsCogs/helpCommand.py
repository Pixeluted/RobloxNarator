import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(
            title='Bot Commands',
            description='Roblox Narrator is an discord bot that is interacting with roblox! You can use this as global (not-logged-in) or as local (you use roblox token to login!)! \n **WE ARE NOT SAVING ANY ROBLOX TOKENS**',
            color=discord.Color.blue()
        )

        embed.add_field(name='**Global Use**',
                        value='!group-info {group-id} - This will return information about the specific group! \n \n !member-count - This will get member count of the global group set!',
                        inline=False)
        embed.add_field(name='**Configuration**',
                        value='!set-group-id {group-id} - This will set your globally choosed group for  this guild! Only admins can use this command!',
                        inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))