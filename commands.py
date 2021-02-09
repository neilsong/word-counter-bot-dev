from discord import channel, message
from discord.ext import commands
import discord

import collections
import datetime
import time
import pprint
import sys
import re
import copy
from disputils import BotEmbedPaginator

from main import *
from decorator import *
from utilities import *

def find_color(ctx):
    # Find the bot's rendered color. If default color or in a DM, return Discord's grey color

    try:
        if ctx.guild.me.color == discord.Color.default():
            color = discord.Color.greyple()
        else:
            color = ctx.guild.me.color
    except AttributeError:  #* If it's a DM channel
        color = discord.Color.greyple()
    return color



class Commands(commands.Cog):
    # Commands for the Word Counter Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @isAllowed()
    @commands.guild_only()
    async def help(self, ctx):

        cmds = sorted([c for c in self.bot.commands if not c.hidden], key=lambda c: c.name)
        
        description = "I keep track of every word a user says. I'm a pretty simple bot to use. My prefix"
        if len(self.bot.prefixes[str(ctx.guild.id)]) > 1:
            description+="es are "
            for i in self.bot.prefixes[str(ctx.guild.id)]:
                if i == self.bot.prefixes[str(ctx.guild.id)][len(self.bot.prefixes[str(ctx.guild.id)])-1]:
                    description += f"and `{i}`"
                else:  
                    description += f"`{i}`" 
                    if len(self.bot.prefixes[str(ctx.guild.id)]) > 2:
                        description += ", "
                    else:
                        description += " "
        elif len(self.bot.prefixes[str(ctx.guild.id)]) == 1:
            description += f" is `{self.bot.prefixes[str(ctx.guild.id)][0]}`"
        else:
            description += " is `!`"
        description += "\n\nHere's a short list of my commands:"
        embed = discord.Embed(
            title="Word Counter Bot: Help Command",
            description= description,
            color=find_color(ctx))
        embed.set_footer(
            text="Note: I don't count words said in the past before I joined this server")
        for c in cmds:
            embed.add_field(name=c.name, value=c.help, inline=False)
 
        await ctx.send(embed=embed)

    @commands.command(aliases=["info"])
    @isAllowed()
    async def about(self, ctx):
        # Some basic info about this bot

        embed = discord.Embed(
            title=str(self.bot.user), description=self.bot.app_info.description +
            f"\n\n**User/Client ID**: {self.bot.app_info.id}", color=find_color(ctx))

        embed.set_thumbnail(url=self.bot.app_info.icon_url)
        from config import ADMINS
        tadmins = ADMINS.copy()
        for i in range(0, len(tadmins)):
            tadmins[i] = await self.bot.fetch_user(tadmins[i])
        tadmins = wordListToString(tadmins)
        tadmins = tadmins.replace('`', '')
        embed.add_field(name="Admins", value=tadmins)
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="User Count", value=len(self.bot.users))
        embed.add_field(
            name="Language",
            value=f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
        embed.add_field(
            name="Library", value="[discord.py](https://github.com/Rapptz/discord.py)")
        embed.add_field(
            name="License",
            value="MIT")
        embed.add_field(
            name="Source Code", value="https://github.com/neilsong/word-counter-bot", inline=False)
        embed.add_field(
            name="Contributors", value="https://bit.ly/3cWYlsn", inline=False)
        embed.add_field(
            name = "Distant Cousin", value="https://github.com/NWordCounter/bot", inline=False)

        await ctx.send(embed=embed)

    async def renderEmbed(self, ctx, lDict: dict, title ,isGlobal: str=None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        description = "\n"
        counter = 1
        for m, c in lDict.items():
            description += (f"**{counter}.** {self.bot.get_user(int(re.sub('[^0-9]', '', m))).mention if bool(re.search('<@(!?)([0-9]*)>',m)) else m } - __{c:,} "
                            f"time{'' if c == 1 else 's'}__\n")
            counter += 1

        description = description.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(description=description, color=find_color(ctx),
                              timestamp=datetime.datetime.utcnow())
        if isGlobal == "global":
            embed.set_author(
                name=title)
        else:
            embed.set_author(
                name=title, icon_url=ctx.guild.icon_url)

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    async def countserver(self, ctx):
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage

        try:
            words=self.bot.serverWords[ctx.guild.id]
        except:
            return await ctx.send("Nothing found? Something must have gone wrong.")
        counter=0

        words={k: v for k, v in sorted(words.items(), key=lambda item: item[1],reverse=True)}
        for w in words:
            if w=="__id":
                continue
            counter+=words[w]
        ct=0
        desc="\n"
        for w in words:
            if w=="__id":
                continue
            try: 
                if w in self.bot.filter[str(ctx.guild.id)]: continue
            except: pass
            ct+=1
            desc+="\n**"+ str(ct) + ".** " + w+" - __"+str(words[w])+" times__"
            if ct==10:
                break
        desc = desc.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(
            description=str(len(words)-1)+" distinct words have been said, with "+str(counter)+" words said in total. (Only showing top 10)"+desc,
            color=find_color(ctx),
            timestamp=datetime.datetime.utcnow())

        embed.set_author(
                name="The Server\'s Word Leaderboard", icon_url=ctx.guild.icon_url)

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
    
    async def globalWords(self,ctx):
        try:
            words=self.bot.serverWords[0].copy()
            try:
                for i in self.bot.filter[str(ctx.guild.id)]:
                    try: words.pop(i)
                    except: continue
            except: pass

        except:
            return await ctx.send("Weird, no words logged yet.")
        
        words=dict(collections.Counter(words).most_common(10))

        description = "\n"
        counter = 1
        for m, c in words.items():
            description += (f"**{counter}.** {m} - __{c:,} "
                            f"time{'' if c == 1 else 's'}__\n")
            counter += 1

        description = description.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(description=description, color=find_color(ctx),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(
            name="Global Most Common Words")

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


    


    async def makeEmbed(self,ctx,words,pageNum,user):
        
        description = "\n"
        counter = 1
        for m, c in words.items():
            description += (f"**{counter+pageNum*15}.** {m} - __{c:,} "
                            f"time{'' if c == 1 else 's'}__\n")
            counter += 1

        description = description.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(description=description, color=find_color(ctx),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(
            name=f"{user.name}'s Most Common Words", icon_url=ctx.author.avatar_url)

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url)
        return embed


    @commands.command()
    @isAllowed()
    async def count(self, ctx, user=None,):
        # Get the number of times a user has said any word
        # Format like this: `count <@mention user>`
        # If requester doesn't mention a user, the bot will get requester's count
        # If requester has global as argument, the bot will get the gobal count

        if(user=="server"):
            return await self.countserver(ctx)
        if(user=="global"):
            return await self.globalWords(ctx)
        words={}
        
        if not user is None:
            try:
                user=self.bot.get_user(int(re.sub("[^0-9]", "", user)))
            except:
                return await ctx.send("Not a valid user.")

        if user is None:
            user = ctx.author
        elif user == self.bot.user:
            return await ctx.send("Man, why would I count my own words?")    
        elif user.bot:
            return await ctx.send("I don't count words said by bots.")
        
        embeds=[]

        if not (user == self.bot.user):
            try:
                words=self.bot.userWords[user.id]

                words={k: v for k, v in sorted(words.items(), key=lambda item: item[1],reverse=True)}
                words.pop('__id')
                try:
                    for i in self.bot.filter[str(ctx.guild.id)]:
                        try: words.pop(i)
                        except: continue
                except: pass
            except:
                return await ctx.send(f"{user.mention} hasn't said anything that I have logged yet.")
        
                
        if not len(words):
            return await ctx.send(f"{user.mention} hasn't said anything that I have logged yet.")

        embeds=[]; count2 = 0; count = 0; nD={}
        for key in words:
            count2+=1
            nD[key]=words[key]
            if count2==15 or count2==len(words):
                embeds.append(await self.makeEmbed(ctx,nD,count,user))
                count+=1

                nD.clear()
                count2=0

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
        #await ctx.send(embed=embed)



    #@count.error
    #async def count_error(self, ctx, exc):
    #    if isinstance(exc, commands.BadArgument):
    #        return await ctx.send(exc)

    @commands.command()
    @isAllowed()
    async def readhistory(self, ctx):
        async for msg in ctx.channel.history(limit=300):
            msgcontent = msg.content.replace("\n", " ")
            print("History: " + msgcontent)
            await main.updateWord(message)
    


    @commands.command()
    @isAllowed()
    async def invite(self, ctx):
        # Sends an invite link

        await ctx.send("Here's my invite link so I can count words on your server too:\n"
                       f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
                       "&scope=bot&permissions=8")

    @commands.command()
    @isAllowed()
    async def stats(self, ctx):
        # View stats

        await ctx.channel.trigger_typing()

        uptime = datetime.datetime.utcnow() - self.bot.started_at

        y = int(uptime.total_seconds()) // 31557600  #* Number of seconds in 356.25 days
        mo = int(uptime.total_seconds()) // 2592000 % 12  #* Number of seconds in 30 days
        d = int(uptime.total_seconds()) // 86400 % 30  #* Number of seconds in 1 day
        h = int(uptime.total_seconds()) // 3600 % 24  #* Number of seconds in 1 hour
        mi = int(uptime.total_seconds()) // 60 % 60  #* etc.
        se = int(uptime.total_seconds()) % 60

        frmtd_uptime = []
        if y != 0:
            frmtd_uptime.append(f"{y}y")
        if mo != 0:
            frmtd_uptime.append(f"{mo}mo")
        if d != 0:
            frmtd_uptime.append(f"{d}d")
        if h != 0:
            frmtd_uptime.append(f"{h}hr")
        if mi != 0:
            frmtd_uptime.append(f"{mi}m")
        if se != 0:
            frmtd_uptime.append(f"{se}s")

        total = 0
        for i, c in self.bot.serverWords[0].items():
            total += c

        embed = discord.Embed(
            description=f"Bot User ID: {self.bot.user.id}",
            timestamp=datetime.datetime.utcnow(),
            color=find_color(ctx))
        embed.add_field(name="Server Count", value=f"{len(self.bot.guilds):,} servers")
        embed.add_field(name="User Count", value=f"{len(self.bot.users):,} unique users")
        embed.add_field(
            name="Channel Count",
            value=f"{len(list(self.bot.get_all_channels()) + self.bot.private_channels):,} "
                  "channels")
        embed.add_field(
            name="Memory Usage",
            value=f"{round(self.bot.process.memory_info().rss / 1000000, 2)} MB")
        embed.add_field(name="Latency/Ping", value=f"{round(self.bot.latency * 1000, 2)}ms")
        embed.add_field(name="Uptime", value=" ".join(frmtd_uptime) + " since last restart")
        embed.add_field(
            name="Number of Users Who Have Said Any Word",
            value=f"{len(self.bot.userWords):,}",
            inline=False)
        embed.add_field(
            name="Total Words Counted",
            value=f"{total:,} ",
            inline=False)
        embed.set_author(name="Word Counter Bot: Statistics", icon_url=self.bot.user.avatar_url)
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(text="These statistics are accurate as of ")

        await ctx.send(embed=embed)

    @commands.command(aliases=["leaderboard", "high"])
    @commands.guild_only()
    @isAllowed()
    async def top(self, ctx, word: str=None, isGlobal: str=None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        if word==None:
            return await ctx.send("Please type a word to search for.\n Ex: `!top lol`")
        try:
            if word in self.bot.filter[str(ctx.guild.id)]:
                return await ctx.send("That word is filtered")
        except: pass
        if isGlobal and not isGlobal == "global":
            return await ctx.send("If you are trying to get the global leaderboard, do `!top lol global`")
        word=word.lower();
        await ctx.channel.trigger_typing()
        leaderboard = {}
        if isGlobal == "global":
            for u, c in self.bot.userWords.items():
                try:
                    leaderboard.update({u: c[word]})
                except:
                    continue
            leaderboard = dict(collections.Counter(leaderboard).most_common(10))
            for u in leaderboard.copy():
                user = await self.bot.fetch_user(u)
                leaderboard[user] = leaderboard.pop(u)
        else:
            async for user in ctx.guild.fetch_members(limit=None):
                try:
                    leaderboard.update({user: self.bot.userWords[user.id][word]})
                except:
                    continue
            leaderboard = dict(collections.Counter(leaderboard).most_common(10))


        print(leaderboard)
        if not len(leaderboard):
            return await ctx.send("No one on this server has said this word yet")

        description = "\n"
        counter = 1
        for m, c in leaderboard.items():
            description += (f"**{counter}.** {m if isGlobal == 'global' else m.mention} - __{c:,} "
                            f"time{'' if c == 1 else 's'}__\n")
            counter += 1

        description = description.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(description=description, color=find_color(ctx),
                              timestamp=datetime.datetime.utcnow())
        if isGlobal == "global":
            embed.set_author(
                name=f"Top Users of \"{word}\"")
        else:
            embed.set_author(
                name=f"Top Users of \"{word}\" in {ctx.guild.name}", icon_url=ctx.guild.icon_url)

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @isAllowed()
    @commands.guild_only()
    async def prefix(self, ctx):
        description = "My prefix"
        if len(self.bot.prefixes[str(ctx.guild.id)]) > 1:
            description+="es: "
            description += wordListToString(self.bot.prefixes[str(ctx.guild.id)])
        elif len(self.bot.prefixes[str(ctx.guild.id)]) == 1:
            description += ": "
            description += wordListToString(self.bot.prefixes[str(ctx.guild.id)])
        else:
            description += ": `!`"
        await ctx.send(description)

    @commands.command()
    @commands.guild_only()
    @isAllowed()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, *, prefixes=""):
        if len(prefixes) > 0:
            prefixlist = prefixes.split(" ")
            self.bot.prefixes.update({str(ctx.guild.id): prefixlist})
            if len(prefixlist) > 1:
                await ctx.send("Prefixes set")
            else:
                await ctx.send("Prefix set")
        else:
            await ctx.send("Please set either a one-character prefix, or multiple one-character prefixes separated by spaces")

    @commands.command()
    @commands.guild_only()
    @isAllowed()
    @commands.has_permissions(manage_guild=True)
    async def addblacklist(self, ctx, *, channels):
        response = ""
        channels = channels.replace("<", "").replace("#", "").replace(">", "").split(" ")
        if len(channels) > 0: 
            for i in channels:
                try:
                    if i in self.bot.blacklist[str(ctx.guild.id)]:
                        response += f"<#{i}> already blacklisted\n"
                        continue
                    self.bot.blacklist[str(ctx.guild.id)].append(int(i))
                except:
                    self.bot.blacklist.update({str(ctx.guild.id) : [int(i)]})
                response += f"<#{i}> added\n"
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await ctx.send(response)

    @commands.command()
    @commands.guild_only()
    @isAllowed()
    @commands.has_permissions(manage_guild=True)
    async def removeblacklist(self, ctx, *, channels):
        response = ""
        channels = channels.replace("<", "").replace("#", "").replace(">", "").split(" ")
        if len(channels) > 0: 
            for i in channels:
                try:
                    self.bot.blacklist[str(ctx.guild.id)].remove(int(i))
                    response += f"<#{i}> removed\n"
                    if len(self.bot.blacklist[str(ctx.guild.id)]) == 0:
                        self.bot.blacklist.pop(str(ctx.guild.id))
                        response += f"The blacklist is now empty\n"
                except:
                    response += f"<#{i}> not blacklisted\n"
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await ctx.send(response)
        
    @commands.command()
    @isAllowed()
    @commands.guild_only()
    async def blacklist(self, ctx):
        blacklist = "Currently blacklisted channel"
        if not str(ctx.guild.id) in self.bot.blacklist.keys():
            await ctx.send("There is no blacklist for this server")
            return
        blacklist += channelListToString(self.bot.blacklist[str(ctx.guild.id)])
        await ctx.send(blacklist)

    @commands.command()
    @commands.guild_only()
    @isAllowed()
    @commands.has_permissions(manage_guild=True)
    async def removefilter(self, ctx, *, words=""):

        for w in trashCharacters:
            words = words.replace(w, " ")
        words=' '.join(words.split())
        words = words.lower()
        
        response = ""
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                try:
                    self.bot.filter[str(ctx.guild.id)].remove(i)
                    response += f"`{i}` removed\n"
                    if len(self.bot.filter[str(ctx.guild.id)]) == 0:
                        self.bot.filter.pop(str(ctx.guild.id))
                        response += f"The filter is now empty\n"
                except:
                    response += f"`{i}` is not in the filter\n"
        else:
            response += "Please remove either one word, or multiple words separated by spaces"
        
        await ctx.send(response)


    @commands.command()
    @commands.guild_only()
    @isAllowed()
    @commands.has_permissions(manage_guild=True)
    async def addfilter(self, ctx, *, words=""):
        for w in trashCharacters:
            words = words.replace(w, " ")
        words=' '.join(words.split())
        words = words.lower()

        response = ""
        added = False
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                try:
                    if i in self.bot.filter[str(ctx.guild.id)]:
                        response += f"`{i}` already in filter\n"
                        continue
                    self.bot.filter[str(ctx.guild.id)].append(i)
                except:
                    self.bot.filter.update({str(ctx.guild.id) : [i]})
                response += f"`{i}` added\n"
        else:
            response += "Please add either one word, or multiple words separated by spaces"

        await ctx.send(response)
        
    @commands.command()
    @isAllowed()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def filter(self, ctx):
        filter = "Current filter: "
        if not str(ctx.guild.id) in self.bot.filter.keys():
            await ctx.send("There is no filter for this server")
            return
        filter += wordListToString(self.bot.filter[str(ctx.guild.id)])
        await ctx.send(filter)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

    # BOT ADMIN COMMANDS
    @commands.command(hidden=True)
    @isaBotAdmin()
    @isAllowed()
    async def edituser(self, ctx, user_id: int, word: str=None, count: int=0):
        # Edit a user's entry in all collections or add a new one
        if not user_id or not word or not count:
            return ctx.send("Parameters: user_id, word, count")

        change = 0
        try:
            change = count - self.bot.userWords[user_id][word]
        except:
            change = count
        
        if count == 0:
            try: self.bot.userWords[user_id].pop(word)
            except: pass
        
        self.bot.userWords[user_id][word] = count
        self.bot.serverWords[ctx.guild.id][word] += change
        self.bot.serverWords[0][word] += change
        
        await ctx.send("Done")
        
    @commands.command(hidden=True)
    @isaBotAdmin()
    @isAllowed()
    async def popdefaultfilter(self, ctx):
        for i in defaultFilter:
            for u in self.bot.userWords:
                try: self.bot.userWords[u].pop(word)
                except: continue
            for u in self.bot.serverWords:
                try: self.bot.serverWords[u].pop(word)
                except: continue
            try: self.bot.serverWords[0].pop(word)
            except: pass
        await ctx.send("Done")
    
    @commands.command(hidden=True)
    @isaBotAdmin()
    @isAllowed()
    async def popword(self, ctx, word: str=None):
        # Pop a word from all collections

        for u in self.bot.userWords:
            try: self.bot.userWords[u].pop(word)
            except: continue
        for u in self.bot.serverWords:
            try: self.bot.serverWords[u].pop(word)
            except: continue
        try: self.bot.serverWords[0].pop(word)
        except: pass
        await ctx.send("Done")

    @commands.command(hidden=True)
    @isaBotAdmin()
    @commands.guild_only()
    @isAllowed()
    async def popuser(self, ctx, user_id: int):
        # Pop a user from all collections

        try:
            for u, c in self.bot.userWords[user_id].items():
                self.bot.serverWords[ctx.guild.id][u] -= c
                self.bot.serverWords[0][u] -= c
            self.bot.userWords.pop(user_id)
            await self.bot.collection.delete_one({"__id": user_id})
            await ctx.send("Done")
        except KeyError as e:
            await ctx.send(f"User `{e}` does not exist or has no words logged yet.")


    # @commands.command(hidden=True)
    # @isaBotAdmin()
    # @isAllowed()
    # async def execute(self, ctx, *, query):
    #     """Execute a query in the database"""

    #     try:
    #         with ctx.channel.typing():
    #             async with self.bot.pool.acquire() as conn:
    #                 result = await conn.execute(query)
    #         await ctx.send(f"Query complete:```{result}```")
    #     except Exception as e:
    #         await ctx.send(f"Query failed:```{e}```")

    @commands.command(aliases=["resetstatus"], hidden=True)
    @isaBotAdmin()
    @isAllowed()
    async def restartstatus(self, ctx):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
            name=f"any Words on {len(self.bot.guilds)} servers",
            type=discord.ActivityType.watching))

        await ctx.send("Reset playing status")

    @commands.command(hidden=True)
    @isaBotAdmin()
    @isAllowed()
    async def setstatus(self, ctx, status):
        """Change the bot's presence"""

        if status.startswith("on"):
            await self.bot.change_presence(status=discord.Status.online)
        elif status.startswith("id"):
            await self.bot.change_presence(status=discord.Status.idle)
        elif status.startswith("d"):
            await self.bot.change_presence(status=discord.Status.dnd)
        elif status.startswith("off") or status.startswith("in"):
            await self.bot.change_presence(status=discord.Status.invisible)
        else:
            await ctx.send("Invalid status")

        await ctx.send("Set new status")

def setup(bot):
    bot.add_cog(Commands(bot))
