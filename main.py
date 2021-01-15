from discord.ext import commands, tasks
import discord
from pymongo import MongoClient
import psutil

import datetime
import re
import os

import config

bot_intents = discord.Intents.default()
bot_intents.members = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="Word Counter Bot",
    case_insensitive=True,
    help_command=None,
    status=discord.Status.invisible,
    intents=bot_intents,
    fetch_offline_members=True
)

bot.process = psutil.Process(os.getpid())
bot.ready_for_commands = False
bot.load_extension("commands")
bot.load_extension("error_handlers")


# DB Schema
# users-db = db
# users = collection
# doc: {
#   id: discord-user-id
#   word_1: count 
# }

async def create_db():
        # Create db in MongoDB if it doesn't already exist.
        bot.collection = await MongoClient(config.MONGO)['users-db']['users']
        async with bot.collection as conn:
            query = conn.find({}, {"_id": 0})

        bot.words = {}
        for i in query:
            bot.words.update({i.get("id"): dict(i)})
        
        print("\nCreating DB")

@bot.event
async def on_connect():
    print("\nConnected to Discord")


@bot.event
async def on_ready():
    await create_db()

    print("\nLogged in as:")
    print(bot.user)
    print(bot.user.id)
    print("-----------------")
    print(datetime.datetime.now().strftime("%m/%d/%Y %X"))
    print("-----------------")
    print("Shards: " + str(bot.shard_count))
    print("Servers: " + str(len(bot.guilds)))
    print("Users: " + str(len(bot.users)))
    print("-----------------\n")

    #update_db.start()
    bot.ready_for_commands = True
    bot.started_at = datetime.datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for any word on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_message(message):
    if not bot.ready_for_commands or message.author.bot:
        return

    if message.guild is not None:
        # Untested for-each, init doc reference only
        for w in message.content:
            if message.author.id not in bot.words:
                bot.words.update(
                    {message.author.id: {w: 0, "id": message.author.id}})
            bot.words[message.author.id][w] += 1
            bot.words[0][w] += 1

    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.invoke(ctx)
    else:
        if bot.user in message.mentions and len(message.mentions) == 2:
            await message.channel.send(f"You need to do `@{bot.user} count <user>` to get the "
                                       f"word count of another user.\nDo `@{bot.user} help` "
                                       "for help on my other commands")
        elif bot.user in message.mentions:
            await message.channel.send(f"Do `@{bot.user} help` for help on my commands")


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@tasks.loop(minutes=5, loop=bot.loop)
async def update_db():
    # Update the MongoDB every 5 minutes
    async with bot.collection as conn:
        for data in bot.words:
            conn.update_one({"id": data.get(id, "total")}, {"$inc": data}, True)



@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx):
    # Reload the bot

    bot.reload_extension("commands")
    bot.reload_extension("error_handlers")
    await ctx.send("Reloaded extensions")


@bot.command(hidden=True)
@commands.is_owner()
async def restartdb(ctx):
    await create_db()
    await ctx.send("Restarted db")


@bot.command(hidden=True)
@commands.is_owner()
async def restartudb(ctx):
    update_db.cancel()
    update_db.start()
    await ctx.send("Cancelled and restarted `update_db()`")


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
    #update_db.cancel()
    print("Closed")
