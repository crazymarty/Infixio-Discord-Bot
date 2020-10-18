import asyncio
from datetime import time

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


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, num: int = None, user: discord.User = None):
        if num:
            if user is None:
                await ctx.channel.purge(limit=num)
                embed = discord.Embed(
                    description=f"Cleared `{num}` messages.",
                    color=embedColor
                )
                embed.set_footer(text=f"Cleared by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await msg.delete()
            else:
                def getAuthor(m):
                    return m.author == user
                await ctx.channel.purge(limit=num, check=getAuthor)
                embed = discord.Embed(
                    description=f"Cleared `{num}` messages from {user.mention}",
                    color=embedColor
                )
                embed.set_footer(text=f"Cleared by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, reason: str = None):
        if member is not None:
            if not member.guild_permissions.manage_messages:
                if reason is not None:
                    try :
                        await member.kick(reason=reason)
                        await ctx.send(embed=simpleEmbed(f"{member.mention} has been kicked by {ctx.author.mention} for `{reason}`"))
                    except discord.Forbidden:
                        await ctx.send(embed=simpleEmbed(f"Missing permissions."))
                else:
                    try:
                        await member.kick(reason=reason)
                        await ctx.send(embed=simpleEmbed(f"{member.mention} has been kicked by {ctx.author.mention} for `Violating Server Rules`"))
                    except discord.Forbidden:
                        await ctx.send(embed=simpleEmbed(f"Missing permissions."))
            else:
                await ctx.send(embed=simpleEmbed(f"You may not kick a moderator"))
        else:
            await ctx.send(embed=simpleEmbed(f"Please specify a user to kick"))
#    @flags.add_flag("--title", type=str, default="Infix Studio Announcement", nargs='+')
#    @flags.add_flag("--desc", type=str, default="An announcement", nargs='+')
#    @flags.command()
#    @has_permissions(administrator=True)
#    async def announce(self, ctx, **flags):
#        data = inf.getInfo()
#        title = "{title!r}".format(**flags)
#        desc = "{desc!r}".format(**flags)
#        title = ' '.join(map(str, title))
#        print(title)
#        desc = ' '.join(map(str, desc))
#        print(desc)
#        if data['announcechannel'] is not None:
#            embed = discord.Embed(
#                title=title,
#                description=desc
#            )
#            embed.color = embedColor
#            await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(administrator=True)
    async def announce(self, ctx):
        data = inf.getInfo()
        if data['announcechannel']:
            embed = discord.Embed(
                title="Infix Studio Announcement",
                description=ctx.message.content
            )
            embed.set_footer(text=f"{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            embed.color = embedColor
            ch = self.client.get_channel(data['announcechannel'])
            await ch.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
