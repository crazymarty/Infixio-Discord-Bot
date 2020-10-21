import json
import random
import sys
import traceback
import aiohttp
import discord
from discord.ext import flags, commands, tasks
from discord.ext.commands import has_permissions
import os


def importJson(data):
    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile)


def getInfo():
    with open('config.json') as jsonFile:
        data = json.load(jsonFile)
    return data


def getPrefix():
    data = getInfo()
    pref = data['prefix']
    return pref


def getToken():
    data = getInfo()
    toke = data['token']
    return toke


prefix = getPrefix()
TOKEN = getToken()
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
embedColor = discord.Colour.gold()

initial_extensions = ['fun', 'moderation', 'config', 'utils']
for extension in initial_extensions:
    client.load_extension(extension)


def simpleEmbed(s):
    embed = discord.Embed(
        color=discord.Colour.gold(),
        description=s,
    )
    return embed


@client.command()
async def ping(ctx):
    await ctx.send(embed=simpleEmbed(f'am alive! `{round(client.latency * 1000)}ms` '))


@client.command()
async def quote(ctx):
    responses = open('quotes.txt').read().splitlines()
    random.seed(a=None)
    response = random.choice(responses)
    await ctx.send(response)


# @client.command()
# async def selfdestruct(ctx):
#    responses = open('sd.txt').read().splitlines()
#    random.seed(a=None)
#    response = random.choice(responses)
#    await ctx.send(response)


@client.event
async def on_command_error(ctx, error):
    p = getPrefix()
    ignored = (commands.CommandNotFound,)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
        return
    if isinstance(error, commands.DisabledCommand):
        error = error
    elif isinstance(error, commands.NoPrivateMessage):
        try:
            error = error
        except discord.HTTPException:
            pass
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':
            error = error

    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    embed = discord.Embed(
        description="Error occurred. Try `" + p + "help` for help. Error: `" + str(error) + "`",
        color=embedColor,
    )
    await ctx.send(embed=embed)


# We delete default help command
client.remove_command('help')


# Embedded help with list and details of commands
@client.command(pass_context=True)
async def help(ctx, arg: str = None):
    data = getInfo()
    pref = data['prefix']
    if arg is None:
        embed = discord.Embed(
            colour=embedColor,
            title="**Infixio Bot Commands**",
            description="Know more about all the features in Infixio bot"
        )
        embed.set_author(name="Help for " + client.user.display_name, icon_url=client.user.avatar_url)
        embed.add_field(name=":smile: Fun", value=f'`{pref}help fun`', inline=True)
        embed.add_field(name=":tools: **Utils**", value=f'`{pref}help utils`', inline=True)
        embed.add_field(name=":gear: **Config**", value=f'`{pref}help config`', inline=True)
        embed.set_footer(text="Official Infix Studio Bot", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    elif arg == "fun":
        embed = discord.Embed(
            colour=embedColor,
            title="**Infixio Bot Commands | :smile: Fun**",
            description="Fun commands to blow out your bordism"
        )
        embed.set_author(name="Help for " + client.user.display_name, icon_url=client.user.avatar_url)
        embed.add_field(name="  •`" + pref + 'meme`', value='Get some cool memes', inline=False)
        embed.set_footer(text="Official Infix Studio Bot", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    elif arg == "utils":
        embed = discord.Embed(
            colour=embedColor,
            title="**Infixio Bot Commands | :tools: Utils**",
            description="Fun commands to blow out your bordism"
        )
        embed.add_field(name="  •`" + pref + 'ping`', value='Returns bot respond time in milliseconds', inline=False)
        embed.add_field(name="  •`" + pref + 'quote`', value='Get an inspiring quote', inline=False)
        embed.add_field(name="  •`" + pref + 'welcome`', value='Get a thanks message for welcoming our bot',
                        inline=False)
        embed.add_field(name="  •`" + pref + 'avatar [user]`', value='Get your or a user\'s avatar', inline=False)
        embed.set_footer(text="Official Infix Studio Bot", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    elif arg == "config":
        embed = discord.Embed(
            colour=embedColor,
            title="**Infixio Bot Commands | :gear: Config**",
            description="Configure server settings and bot settings"
        )
        embed.add_field(name="  •`" + pref + 'setprefix <prefix>`', value='Set bot command prefix', inline=False)
        embed.add_field(name="  •`" + pref + 'setslowmode <time in seconds>`',
                        value='Set slowmode for all the channels in the server', inline=False)
        embed.set_footer(text="Official Infix Studio Bot", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)


@client.command()
async def welcome(ctx):
    await ctx.send(
        embed=simpleEmbed(f'Thanks For the welcome! am glad that my developer made me to handle such lovely people on '
                          f'this server !'))


@client.command()
async def avatar(ctx, user: discord.Member = None):
    if user:
        embed = discord.Embed(
            title=user.display_name + "'s avatar",
            color=embedColor,
        )
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=ctx.message.author.display_name + "'s avatar",
            color=embedColor
        )
        embed.set_image(url=ctx.message.author.avatar_url)


def getSeconds():
    data = getInfo()
    seconds = data['automeme_seconds']
    return seconds


print(getSeconds())


@tasks.loop(seconds=getSeconds())
async def my_timer():
    data = getInfo()
    channel = client.get_channel(data['automeme_channel'])
    if channel is not None:
        session = aiohttp.ClientSession()
        async with session.get("https://meme-api.herokuapp.com/gimme") as r:
            jsonFo = await r.json()
        await session.close()
        embed = discord.Embed(
            color=embedColor
        )
        embed.set_image(url=jsonFo["url"])
        await channel.send(embed=embed)


@client.event
async def on_ready():
    guild = client.get_guild(id=736860059971223613)
    av = await guild.icon_url.read()
    #    await client.user.edit(avatar=av)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Infix Studio"))
    my_timer.start()


bw = getInfo()
badWords = bw['badWords']


# @client.event
# async def on_message(ctx):
#    print(f"[{ctx.channel}] {ctx.author.display_name} > {ctx.content}")


@client.event
async def on_message(msg):
    if msg.author.id != 270904126974590976:
        msgg = msg.content.split(" ")
        if any(i in msgg for i in badWords):
            channel = client.get_channel(747346000380690472)
            await msg.delete()
            embed = discord.Embed(
                description=f"**Message:** {msg.content} \n **Channel**: <#{msg.channel.id}>",
                color=embedColor,
            )
            user = client.get_user(msg.author.id)
            embed.set_author(name=f"{msg.author} swore", icon_url=user.avatar_url)
            await msg.channel.send(embed=simpleEmbed(f"Swearing is not allowed {msg.author.mention}"))
            await channel.send(embed=embed)
    await client.process_commands(msg)


# @client.event
# async def on_message(msg):
#    if not msg.guild:
#        channel = client.get_channel(744813616695607338)
#        await channel.send(f"[DM] {msg.author} » {msg.content})")
#        data = getInfo()
#        data['lastPersonToDm'] = msg.author
#        importJson(data)
#    await client.process_commands(msg)

@client.listen('on_message')
async def fo(msg: discord.Message):
    if not msg.guild:
        if msg.author != client.user:
            channel = client.get_channel(747109686766993498)
            await channel.send(f"**[DM]** {msg.author} » `{msg.content}`")
            data = getInfo()
            data['lastPersonToDm'] = msg.author.id
            importJson(data)
    pass


@client.listen('on_message')
async def foo(msg: discord.Message):
    if msg.guild:
        if msg.author != client.user:
            data = getInfo()
            user = data['lastPersonToDm']
            if msg.channel.id == 747109686766993498:
                user = client.get_user(user)
                await user.send(f"**[ADMIN]** {msg.author} » `{msg.content}`")
    pass


@client.listen('on_message_delete')
async def fooo(msg: discord.Message):
    data = getInfo()
    print("test 5")
    if data['logch']:
        print("test 4")
        ch = client.get_channel(data['logch'])
        chan = msg.channel
        guild = chan.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            print("test 1")
            if not entry.target.bot:
                print("test 3")
                embed = discord.Embed(
                    description=f"Message deleted in <#{chan.id}>"
                )
                embed.color = embedColor
                embed.set_author(name="Infix Log Message", icon_url=client.user.avatar_url)
                url = entry.user.avatar_url
                embed.add_field(name=f"**Message by:**", value=f"{entry.target.mention}")
                embed.add_field(name=f"**Message:**", value=f"{msg.content}")
                embed.set_footer(text=f"Deleted by {entry.user}", icon_url=url)
                await ch.send(embed=embed)
    pass

client.run(os.environ['token'])
