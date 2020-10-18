import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import infixio as inf

embedColor = inf.embedColor


def simpleEmbed(s):
    embed = discord.Embed(
        color=discord.Colour.gold(),
        description=s,
    )
    return embed


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator=True)
    async def setautomeme(self, ctx, arg: str):
        if arg == "off":
            data = inf.getInfo()
            data['automeme_channel'] = ""
            inf.importJson(data)
            await ctx.send(embed=simpleEmbed(f"Auto memes has been disabled!"))
        elif arg == "here":
            channel = ctx.channel
            data = inf.getInfo()
            data['automeme_channel'] = channel.id
            inf.importJson(data)
            await ctx.send(embed=simpleEmbed(f"Auto memes channel has been set to `{channel}`"))
        else:
            try:
                id = int(arg)
                channel = self.client.get_channel(id)
                data = inf.getInfo()
                data['automeme_channel'] = channel.id
                inf.importJson(data)
                await ctx.send(embed=simpleEmbed(f"Auto memes channel has been set to `{channel}`"))
            except:
                await ctx.send(embed=simpleEmbed("Invalid argument. Argument should be a `channel id` or `here`"))

    @commands.command()
    @has_permissions(administrator=True)
    async def setprefix(self, ctx, pref: str = None):
        if pref != "":
            data = inf.getInfo()
            data['prefix'] = pref
            inf.importJson(data)
            inf.client.command_prefix = commands.when_mentioned_or(pref)
            await ctx.send(embed=simpleEmbed("Prefix has been changed to `" + pref + "`"))

    @commands.command()
    @has_permissions(manage_channels=True)
    async def setslowmode(self, ctx, sec: int = None):
        if sec is not None:
            if sec / 5 == 1:
                guild = self.client.get_guild(id=ctx.guild.id)
                for channel in guild.channels:
                    if channel.type == discord.ChannelType.text:
                        await channel.edit(slowmode_delay=5)
                await ctx.send(embed=simpleEmbed(f"Slow mode has been enabled with `" + str(sec) + " seconds` delay"))
            elif sec == 0:
                guild = self.client.get_guild(id=ctx.guild.id)
                for channel in guild.channels:
                    if channel.type == discord.ChannelType.text:
                        await channel.edit(slowmode_delay=0)
                await ctx.send(embed=simpleEmbed("Slow mode has been disabled!"))

    @commands.command()
    @has_permissions(administrator=True)
    async def setannouncech(self, ctx, ch: discord.TextChannel):
        data = inf.getInfo()
        data['announcechannel'] = ch.id
        inf.importJson(data)
        channel = self.client.get_channel(data['announcechannel'])
        embed = discord.Embed(
            title="Infixio | Announcement Channel Updated",
            description=f"Announcement channel has been set to {channel}",
        )
        embed.color=embedColor
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Config(client))
