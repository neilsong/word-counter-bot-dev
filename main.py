from discord.ext import commands
import discord
import psutil
import datetime
import re
import os
import sys
import codecs
import config
import uvloop
from decorator import *
from constants import *
from utilities import insert, get_prefix


uvloop.install()
bot_intents = discord.Intents.default()
bot_intents.members = True


bot = commands.Bot(
    command_prefix=(get_prefix),
    description="Word Counter Bot",
    case_insensitive=True,
    help_command=None,
    status=discord.Status.invisible,
    intents=bot_intents,
    fetch_offline_members=True,
)


@bot.check
def isAllowed(ctx):
    try:
        if str(ctx.message.channel.id) in ctx.bot.blacklist[str(ctx.guild.id)]:
            return False
        else:
            return True
    except:
        return True


# Loading extensions
bot.process = psutil.Process(os.getppid())
bot.ready_for_commands = False
bot.load_extension("commands")
bot.load_extension("error_handlers")
bot.load_extension("management")
bot.load_extension("info")
bot.load_extension("admin")
bot.defaultFilter = defaultFilter


@bot.event
async def on_connect():
    print("\nConnected to Discord")


@bot.event
async def on_ready():
    from db import create_db, start_workers

    await create_db()

    print("\nLogged in as:")
    print(bot.user)
    print(bot.user.id)
    print("-----------------")
    print(datetime.datetime.now().strftime("%m/%d/%Y %X"))
    print("-----------------")
    # print("Shards: " + str(bot.shard_count))
    print("Servers: " + str(len(bot.guilds)))
    print("Users: " + str(len(bot.users)))
    print("-----------------\n")

    await start_workers()
    bot.ready_for_commands = True
    bot.started_at = datetime.datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            name=f"for any word on {len(bot.guilds)} servers",
            type=discord.ActivityType.watching,
        ),
    )


async def updateWord(message):
    msgcontent = message.content.lower()
    for w in trashCharacters:
        msgcontent = msgcontent.replace(w, " ")
    result = msgcontent.split()

    if not result:
        return
    if result[0] == "":
        return
    if bot.userLastMsg.get(message.author.id, "") == msgcontent:
        return
    bot.userLastMsg.update({message.author.id: msgcontent})
    for w in result:
        if "!" in w:
            if not re.search("^<@!\d{18}[>$]", w):
                w = w.replace("!", "")
        if w in defaultFilter:
            continue
        try:
            if w in bot.filter[message.guild.id]:
                continue
        except:
            pass
        if w == "":
            continue
        # print(w)
        # print("\n")
        if message.guild.id not in bot.serverWords:
            bot.serverWords.update({message.guild.id: {w: 0, "__id": message.guild.id}})
        elif w not in bot.serverWords[message.guild.id]:
            bot.serverWords[message.guild.id].update({w: 0, "__id": message.guild.id})
        bot.serverWords[message.guild.id][w] += 1
        await insert(state=4, id=message.guild.id, word=w)
        if message.author.id not in bot.userWords:
            bot.userWords.update({message.author.id: {w: 0, "__id": message.author.id}})
        elif w not in bot.userWords[message.author.id]:
            bot.userWords[message.author.id].update({w: 0, "__id": message.author.id})
        bot.userWords[message.author.id][w] += 1
        await insert(state=3, id=message.author.id, word=w)
        if 0 not in bot.serverWords:
            bot.serverWords.update({0: {w: 0, "__id": 0}})
        elif w not in bot.serverWords[0]:
            bot.serverWords[0].update({w: 0, "__id": 0})
        bot.serverWords[0][w] += 1
        await insert(state=4, id=0, word=w)


# this command only works in this file
@bot.command()
@isaBotAdmin()
async def readhistory(ctx):
    f = codecs.open("serverMessages.txt", "w", "utf-8")
    # open and read the file after the appending:
    for channel in ctx.guild.text_channels:
        print(channel.name)
        if "bots" in channel.category.lower():
            continue
        async for msg in channel.history(
            limit=99999999999
        ):  # .flatten() to recive as an array

            msgcontent = msg.content.replace("\n", " ")
            if not msgcontent:
                continue
            if not msg.author.bot:
                f.write(str(msg.author.id) + msgcontent + "\n")
                await updateWord(msg)
            # print("History: " + msgcontent)

    f.close()

    # f = open("serverMessages.txt", "r")
    print("done")


@bot.event
async def on_message(message):
    if not bot.ready_for_commands or message.author.bot:
        return
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.invoke(ctx)
    elif message.guild is not None:
        await updateWord(message)


@bot.event
async def on_guild_channel_delete(channel):
    try:
        bot.blacklist.remove(channel.id)
    except:
        pass


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            name=f"for words on {len(bot.guilds)} servers",
            type=discord.ActivityType.watching,
        ),
    )


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            name=f"for words on {len(bot.guilds)} servers",
            type=discord.ActivityType.watching,
        ),
    )
    try:
        bot.prefixes.pop(str(guild.id))
        bot.filter.pop(str(guild.id))
        bot.blacklist.pop(str(guild.id))
    except:
        pass


try:
    bot.loop.run_until_complete(bot.start(config.TOKEN))
except KeyboardInterrupt:
    print("\nClosing")
    bot.loop.run_until_complete(bot.change_presence(status=discord.Status.invisible))
    for e in bot.extensions.copy():
        bot.unload_extension(e)
    print("Logging out")
    bot.loop.run_until_complete(bot.logout())
finally:
    from db import cancel_workers

    bot.loop.run_until_complete(cancel_workers())
    print("\nClosed")
    sys.exit(1)
