from discord.ext import commands, tasks
import discord
import motor.motor_asyncio
import psutil
from random import shuffle
import datetime
import re
import os

import config

bot_intents = discord.Intents.default()
bot_intents.members = True


custom_prefixes = []
default_prefixes = ['duckbot ','spedbot ','!']
async def determine_prefix(bot, message):
    guild = message.guild
    #Only allow custom prefixes in server
    if guild:
        return custom_prefixes + default_prefixes
    else:
        return default_prefixes

bot = commands.Bot(
    command_prefix=determine_prefix,
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

# bot.userWords
# {12345667890: {'hi': 1, 'id': 428563260170567700, 'YOOOOOOOOOO': 1, 'IT': 1, 'WORKS': 1, 'POGU': 1}, 
# 0: {'hi': 1, 'YOOOOOOOOOO': 1, 'IT': 1, 'WORKS': 1, 'POGU': 1}}
async def create_db():
        # Create db in MongoDB if it doesn't already exist.
        bot.collection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)['users-db']['users']
        bot.userWords = {}
        async for i in bot.collection.find({}, {"_id": 0}):
           bot.userWords.update({i.get("__id"): dict(i)})           
        
        bot.serverCollection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)['servers-db']['servers']
        bot.serverWords = {}
        async for i in bot.serverCollection.find({}, {"_id": 0}):
           bot.serverWords.update({i.get("__id"): dict(i)})   

        print("\n")
        print(bot.userWords)
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

    update_db.start()
    bot.ready_for_commands = True
    bot.started_at = datetime.datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        name=f"for any word on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


def listToString(s):  
    str1 = " " 
    return (str1.join(s)) 

@bot.event
async def on_message(message):
   
    if not bot.ready_for_commands or message.author.bot:
        return

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
        elif message.guild is not None:
            msgcontent = message.content.replace("\n", " ")
            trashCharacters=[".","/","\\","\"","]","[","|","_","+","{","}",",","= ","*","&","^","~","`","?", "$"]
            for w in trashCharacters:
                msgcontent =msgcontent.replace(w, " ")
            msgcontent=' '.join(msgcontent.split())
            msgcontent=msgcontent.lower()
            result= msgcontent.split(" ")
            #result = listToString(result).split("\n")
            #print(result)
            if result[0]=="":
                return
            for w in result:
                #print(w)
                #print("\n")
                if message.guild.id not in bot.serverWords:
                    bot.serverWords.update({message.guild.id: { w: 0, "__id": message.guild.id }})
                elif w not in bot.serverWords[message.guild.id]:
                    bot.serverWords[message.guild.id].update({ w: 0, "__id": message.guild.id })
                bot.serverWords[message.guild.id][w] += 1


                if message.author.id not in bot.userWords:
                    bot.userWords.update({message.author.id: { w: 0, "__id": message.author.id }})
                elif w not in bot.userWords[message.author.id]:
                    bot.userWords[message.author.id].update({ w: 0, "__id": message.author.id })
                bot.userWords[message.author.id][w] += 1


                if 0 not in bot.serverWords:
                    bot.serverWords.update({ 0: { w: 0, "__id": 0}})
                elif w not in bot.serverWords[0]:
                    bot.serverWords[0].update({ w: 0, "__id": 0})
                bot.serverWords[0][w] += 1



@bot.event
async def on_guild_join(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@tasks.loop(minutes=2, loop=bot.loop)
async def update_db():
    # Update the MongoDB every 5 minutes
    print("\nUpdating")
    for data in list(bot.userWords):
        await bot.collection.update_one({"__id": data}, {'$set': bot.userWords[data]}, True)
    for data in list(bot.serverWords):
        await bot.serverCollection.update_one({"__id": data}, {'$set': bot.serverWords[data]}, True)



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
    update_db.cancel()
    print("Closed")
