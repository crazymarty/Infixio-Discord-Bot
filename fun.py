import aiohttp
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


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        session = aiohttp.ClientSession()
        async with session.get("https://meme-api.herokuapp.com/gimme") as r:
            jsonFo = await r.json()
        await session.close()
        embed = discord.Embed(
            color=embedColor
        )
        embed.set_image(url=jsonFo["url"])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
