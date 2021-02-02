from discord.ext import commands, tasks
import discord
import motor.motor_asyncio
import psutil
from random import shuffle
import datetime
import re
import os
import sys
import config
from decorator import *

bot_intents = discord.Intents.default()
bot_intents.members = True

trash_words = ['and','is','the','a','as','am','it','to']
trashCharacters=[".","/","\\","\"","]","[","|","_","+","{","}",",","= ","*","&","^","~","`","?", "$", " - "]
default_prefix = ['!']

def get_prefix(bot, message):
    try:
        return bot.prefixes[str(message.guild.id)]
    except: 
        return default_prefix
  

bot = commands.Bot(
    command_prefix=(get_prefix),
    description="Word Counter Bot",
    case_insensitive=True,
    help_command=None,
    status=discord.Status.invisible,
    intents=bot_intents,
    fetch_offline_members=True
)

bot.process = psutil.Process(os.getppid())
bot.ready_for_commands = False
bot.load_extension("commands")
bot.load_extension("error_handlers")

# DB Schema

# db = users-db
# collection = users
# doc: {
#   __id: discord-user-id
#   word_1: count 
# }

# db = servers-db
# collection = servers
# doc: {
#   __id: discord-server-id
#   word_1: count
# }
# global doc: {
#   __id: 0
#   word_1: count
# }
# prefixes doc: {
#   _id: 'prefixes'
#   discord-server-id: list of prefixes
# }
# blacklist doc: {
#   _id: 'blacklist'
#   discord-server-id: blacklist of channels
# }
# whitelist doc: {
#   _id: 'whitelist'
#   discord-server-id: blacklist of channels
# }

# In-memory dict schemas
# bot.userWords
# {12345667890: {'hi': 1, '__id': 1234567890, 'YOOOOOOOOOO': 1, 'IT': 1, 'WORKS': 1, 'POGU': 1}}

# bot.serverWords
# {1234567890: {'hi': 1, '__id': 1234567890, 'YOOOOOOOOOO': 1, 'IT': 1, 'WORKS': 1, 'POGU': 1}, 
# 0: {'hi': 1, '__id': 0, 'YOOOOOOOOOO': 1, 'IT': 1, 'WORKS': 1, 'POGU': 1}}
# __id : 0 represents global count

# bot.prefixes
# {'__id': 'prefixes', '1234567890': {'!', '#', '$'}}

# bot.blacklist
# {'__id': 'blacklist', '1234567890': {'0987654321'}}

async def create_db():
        # Create db in MongoDB if it doesn't already exist.
        print("\nCreating or Fetching DB")
        bot.collection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)['users-db']['users']
        bot.userWords = {}
        bot.userLastMsg = {}
        
        async for i in bot.collection.find({}, {"_id": 0}):
           bot.userWords.update({i.get("__id"): dict(i)})           
        
        bot.serverCollection = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO)['servers-db']['servers']
        bot.serverWords = {}
        bot.prefixes = {"__id": "prefixes"}
        async for i in bot.serverCollection.find({}, {"_id": 0}):
            if(i.get("__id") == "prefixes"):
                bot.prefixes.update(dict(i))
                continue
            bot.serverWords.update({i.get("__id"): dict(i)})
        print("\nNumber of Users: "+str(len(bot.userWords))+"\nNumber of Servers: "+str(len(bot.serverWords) - 1))
        

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


async def updateWord(message):
    msgcontent = message.content.replace("\n", " ")
    for w in trashCharacters:
        msgcontent = msgcontent.replace(w, " ")
    msgcontent=' '.join(msgcontent.split())
    msgcontent=msgcontent.lower()
    
    result= msgcontent.split(" ")
    #result = listToString(result).split("\n")
    #print(result
    # print(msgcontent)
    # print(bot.userLastMsg.get(message.author.id,'')
    if result[0]=="":
        return
    if bot.userLastMsg.get(message.author.id,'') == msgcontent:
        return
    bot.userLastMsg.update({message.author.id : msgcontent})
    for w in result:
        if '!' in w:
            if not re.search("^<@!\d{18}[>$]", w):
                w=w.replace("!", "")
        for trash in trash_words:
            if w == trash: return        
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
    elif message.guild is not None:
        await updateWord(message)
            


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))
    try:
        bot.prefixes.pop(str(guild.id))
    except:
        pass


@tasks.loop(minutes=2, loop=bot.loop)
async def update_db():
    # Update the MongoDB every 2 minutes
    print("\nStart Updating")
    for data in list(bot.userWords):
        await bot.collection.update_one({"__id": data}, {'$set': bot.userWords[data]}, True)
    for data in list(bot.serverWords):
        await bot.serverCollection.update_one({"__id": data}, {'$set': bot.serverWords[data]}, True)
    if bot.prefixes: await bot.serverCollection.update_one({"__id": 'prefixes'}, {'$set': bot.prefixes}, True)
    print("\nDone Updating")


# Operational commands

@bot.command(hidden=True)
@isaBotAdmin()
async def reload(ctx):
    # Reload the bot
    bot.reload_extension("commands")
    bot.reload_extension("error_handlers")
    await ctx.send("Reloaded extensions")


@bot.command(hidden=True)
@isaBotAdmin()
@isAllowed()
async def restartdb(ctx):
    await create_db()
    await ctx.send("Restarted db")


@bot.command(hidden=True)
@isAllowed()
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
    sys.exit(1)