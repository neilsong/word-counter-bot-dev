from discord.ext import commands
import discord
import psutil
import datetime
import re
import os
import sys
import codecs
import config
import signal

from decorator import *
from constants import *
from utilities import (
    insert,
    get_prefix,
    processTrash,
    removeItem,
    splitWords,
    processWord,
    processSpecial,
)

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


# Write PID
bot.process = psutil.Process(os.getpid())
f = codecs.open("pid", "w+", "utf-8")
f.truncate(0)
f.close()
f = codecs.open("pid", "w", "utf-8")
f.write(str(os.getpid()))
f.close()


class GracefulExit(SystemExit):
    code = 1


# SIGINT Handler
def raise_graceful_exit(sig, frame):
    print("\nReceived Signal")
    raise GracefulExit()


# Loading extensions
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

    msgcontent = await processSpecial(message)
    msgcontent = processTrash(msgcontent)
    result = splitWords(msgcontent)

    if not result:
        return
    if result[0] == "":
        return
    if bot.userLastMsg.get(message.author.id, "") == msgcontent:
        return
    bot.userLastMsg.update({message.author.id: msgcontent})

    for w in result:
        if w in defaultFilter:
            continue
        if w == "":
            continue

        await processWord(message, w)


# this command only works in this file
@bot.command()
@isaBotAdmin()
async def readhistory(ctx):
    f = codecs.open(f"serverMessages.txt", "w+", "utf-8")
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
    removeItem(bot.blacklist, str(channel.id), str(channel.guild.id))
    try:
        value = bot.blacklist[str(channel.guild.id)]
        await insert(state=1, id=str(channel.guild.id), value=value)
    except:
        await bot.serverCollection.update_one(
            {"__id": "blacklist"}, {"$unset": {str(channel.guild.id): 1}}
        )


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


signal.signal(signal.SIGINT, raise_graceful_exit)
signal.signal(signal.SIGTERM, raise_graceful_exit)
try:
    bot.loop.run_until_complete(bot.start(config.TOKEN))
except GracefulExit:
    pass
finally:
    print("\nClosing")
    bot.loop.run_until_complete(bot.change_presence(status=discord.Status.invisible))
    from db import cancel_workers

    bot.loop.run_until_complete(cancel_workers())
    print("Unloading Extensions")
    for e in bot.extensions.copy():
        bot.unload_extension(e)
    print("\nLogging out")
    bot.loop.run_until_complete(bot.logout())
    print("\nClosed\n")
    sys.exit(0)
