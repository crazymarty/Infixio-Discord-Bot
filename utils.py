import discord
from discord.ext import commands

from infixio import embedColor

embedColor = embedColor


def simpleEmbed(s):
    embed = discord.Embed(
        color=discord.Colour.gold(),
        description=s,
    )
    return embed


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=0)
        await ctx.send(embed=simpleEmbed(f"Invite your friends with this link `{link}`"))

    #@commands.command()
    #async def guildimg(self, ctx):
    #    embed = discord.Embed(
    #        description="test"
    #    )
    #    guild = ctx.guild
    #    url = guild.icon_url
    #    embed.set_image(url=url)
    #    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Utils(client))
