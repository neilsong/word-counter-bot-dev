from discord.ext import commands
import discord

import collections
import datetime
import time
import pprint
import sys
import re


from main import custom_prefixes, default_prefixes
from decorator import *

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
    @banFromChannel()
    async def help(self, ctx):

        cmds = sorted([c for c in self.bot.commands if not c.hidden], key=lambda c: c.name)

        embed = discord.Embed(
            title="Word Counter Bot: Help Command",
            description="I keep track of every word a user says. I'm a "
                        "pretty simple bot to use. My prefix is an @mention, meaning you'll have "
                        f"to put {self.bot.user.mention} before every command."
                        "\n\nHere's a short list of my commands:",
            color=find_color(ctx))
        embed.set_footer(
            text="Note: I don't count words said in the past before I joined this server")
        for c in cmds:
            embed.add_field(name=c.name, value=c.help, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["info"])
    @banFromChannel()
    async def about(self, ctx):
        # Some basic info about this bot

        embed = discord.Embed(
            title=str(self.bot.user), description=self.bot.app_info.description +
            f"\n\n**User/Client ID**: {self.bot.app_info.id}", color=find_color(ctx))

        embed.set_thumbnail(url=self.bot.app_info.icon_url)
        embed.add_field(name="Owner", value=self.bot.app_info.owner)
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
            name="Source Code", value="https://github.com/neilsong/bot-word-counter", inline=False)
        embed.add_field(
            name = "Distant Cousin", value="https://github.com/NWordCounter/bot", inline=False)

        await ctx.send(embed=embed)

    async def renderEmbed(self, ctx, lDict: dict, title ,isGlobal: str=None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        description = "\n"
        counter = 1
        for m, c in lDict.items():
            description += (f"**{counter}.** {m.mention if bool(re.search('<@(!?)([0-9]*)>',m)) else m } - __{c:,} "
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



    @commands.command()
    @banFromChannel()
    async def countserver(self, ctx):
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
            ct+=1
            desc+="\n**"+ str(ct) + ". " + w.mention+"** - "+str(words[w])
            if ct==10:
                break
        
        embed = discord.Embed(
            title="The Server\'s Word Leaderboard",
            description=str(len(words)-1)+" distinct words have been said, with "+str(counter)+" words said in total. (Only showing top 10)"+desc,
            color=find_color(ctx))

        embed.set_footer(text="Note: I don't count words said in the past before I joined this server")
        
        await ctx.send(embed=embed)

    @commands.command()
    @banFromChannel()
    async def prefix(self, ctx):
        await ctx.send("The prefix(es) for this bot as of now are: "+ (' '.join(default_prefixes) + ' ' + ' '.join(custom_prefixes)))


    @commands.command()
    @banFromChannel()
    async def count(self, ctx, user=None):
        # Get the number of times a user has said any word
        # Format like this: `count <@mention user>`
        # If requester doesn't mention a user, the bot will get requester's count
        #user=user.lower()
        #if user=="server":
        #    return countserver(self,ctx)
        #if user="global":
        #    user='0'

        if user is None:
            user = ctx.author
        elif user == self.bot.user:
            return await ctx.send("Man, why would I count my own words?")    
        elif user.bot:
            return await ctx.send("I don't count words said by bots.")

        if not (user == self.bot.user):
            try:
                words=self.bot.userWords[user.id]
            except:
                return await ctx.send(f"{user.mention} hasn't said anything that I have logged yet.")
        
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
            ct+=1
            desc+="\n**"+ str(ct) + ".  " + w+"** - "+str(words[w])
            if ct==10:
                break

        embed = discord.Embed(
            title=user.name+"\'s Word Counts",
            description=str(len(words)-1)+" distinct words have been said, with "+str(counter)+" words said in total. (Only showing top 10)"+desc,
            color=find_color(ctx))

        embed.set_footer(text="Note: I don't count words said in the past before I joined this server")
        
        await ctx.send(embed=embed)



    @count.error
    async def count_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument):
            return await ctx.send(exc)

    @commands.command()
    @banFromChannel()
    async def readhistory(self, ctx):
        async for msg in ctx.channel.history(limit=300):
            msgcontent = msg.content.replace("\n", " ")
            print("History: " + msgcontent)
            trashCharacters=[".","/","\\","\"","]","[","|","_","+","{","}",",","= ","*","&","^","~","`","?", "$"]
            for w in trashCharacters:
                msgcontent = msgcontent.replace(w, " ")
            msgcontent=' '.join(msgcontent.split())
            msgcontent=msgcontent.lower()
            
            result= msgcontent.split(" ")
            #result = listToString(result).split("\n")
            #print(result)

            # print(msgcontent)
            # print(self.bot.userLastMsg.get(msg.author.id,''))

            if result[0]=="":
                return
            if self.bot.userLastMsg.get(msg.author.id,'') == msgcontent:
                return
            self.bot.userLastMsg.update({msg.author.id : msgcontent})

            for w in result:
                #print(w)
                #print("\n")    
                if msg.guild.id not in self.bot.serverWords:
                    self.bot.serverWords.update({msg.guild.id: { w: 0, "__id": msg.guild.id }})
                elif w not in self.bot.serverWords[msg.guild.id]:
                    self.bot.serverWords[msg.guild.id].update({ w: 0, "__id": msg.guild.id })
                self.bot.serverWords[msg.guild.id][w] += 1


                if msg.author.id not in self.bot.userWords:
                    self.bot.userWords.update({msg.author.id: { w: 0, "__id": msg.author.id }})
                elif w not in self.bot.userWords[msg.author.id]:
                    self.bot.userWords[msg.author.id].update({ w: 0, "__id": msg.author.id })
                self.bot.userWords[msg.author.id][w] += 1


                if 0 not in self.bot.serverWords:
                    self.bot.serverWords.update({ 0: { w: 0, "__id": 0}})
                elif w not in self.bot.serverWords[0]:
                    self.bot.serverWords[0].update({ w: 0, "__id": 0})
                self.bot.serverWords[0][w] += 1
    


    @commands.command()
    @banFromChannel()
    async def invite(self, ctx):
        # Sends an invite link

        await ctx.send("Here's my invite link so I can count words on your server too:\n"
                       f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
                       "&scope=bot&permissions=8")

    @commands.command()
    @banFromChannel()
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
    @banFromChannel()
    async def top(self, ctx, word: str=None, isGlobal: str=None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        if word==None:
            return await ctx.send("Please type a word to search for.\n Ex: `!top lol`")

        await ctx.channel.trigger_typing()
        leaderboard = {}
        if isGlobal == "global":
            for u, c in self.bot.userWords.items():
                try:
                    leaderboard.update({self.bot.get_user(u): c[word]})
                except:
                    continue
            leaderboard = dict(collections.Counter(leaderboard).most_common(10))
        else:
            async for user in ctx.guild.fetch_members(limit=None):
                try:
                    leaderboard.update({user: self.bot.userWords[user.id][word]})
                except:
                    continue
            leaderboard = dict(collections.Counter(leaderboard).most_common(10))

        if not len(leaderboard):
            return await ctx.send("No one on this server has said this word yet")
            
        description = "\n"
        counter = 1
        for m, c in leaderboard.items():
            description += (f"**{counter}.** {m if word == 'global' else m.mention} - __{c:,} "
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


    @top.error
    async def top_error(self, ctx, exc):
        if isinstance(exc, commands.NoPrivateMessage):
            return await ctx.send(exc)


    @commands.command()
    @commands.guild_only()
    @banFromChannel()
    async def setprefix(self, ctx, *, prefixes=""):
        if len(prefixes) > 0:
             custom_prefixes.clear
             custom_prefixes.append(prefixes + " " if len(prefixes) != 1 else prefixes)
             await ctx.send("Prefixes set!")
        
        else:
             await ctx.send("Please set a one-character prefix")
        



    @commands.command(hidden=True)
    @isaBotAdmin()
    @banFromChannel()
    async def edituser(self, ctx, user_id: int, word: str=None, count: int=0):
        # Edit a user's entry in all collections or add a new one
        if not user_id or not word or not count:
            return ctx.send("Parameters: user_id, word, count")

        change = 0
        try:
            change = count - self.bot.userWords[user_id][word]
        except:
            change = count
        
        if (count == 0):
            try: self.bot.userWords[user_id].pop(word)
            except: pass
        
        self.bot.userWords[user_id][word] = count
        self.bot.serverWords[ctx.guild.id][word] += change
        self.bot.serverWords[0][word] += change
        
        await ctx.send("Done")

    
    @commands.command(hidden=True)
    @isaBotAdmin()
    async def popword(self, ctx, word: str=None):
        # Pop a word from all collections

        for u in self.bot.userWords:
            try: self.bot.userWords[u].pop(word)
            except: continue
        for u in self.bot.serverWords:
            try: self.bot.serverWords[u].pop(word)
            except: continue
        await ctx.send("Done")

    @commands.command(hidden=True)
    @isaBotAdmin()
    @banFromChannel()
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


    @commands.command(hidden=True)
    @isaBotAdmin()
    @banFromChannel()
    async def execute(self, ctx, *, query):
        """Execute a query in the database"""

        try:
            with ctx.channel.typing():
                async with self.bot.pool.acquire() as conn:
                    result = await conn.execute(query)
            await ctx.send(f"Query complete:```{result}```")
        except Exception as e:
            await ctx.send(f"Query failed:```{e}```")

    @commands.command(aliases=["resetstatus"], hidden=True)
    @isaBotAdmin()
    @banFromChannel()
    async def restartstatus(self, ctx):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
            name=f"any Words on {len(self.bot.guilds)} servers",
            type=discord.ActivityType.watching))

        await ctx.send("Reset playing status")

    @commands.command(hidden=True)
    @isaBotAdmin()
    @banFromChannel()
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

    @commands.command(hidden=True)
    @isaBotAdmin()
    @banFromChannel()

    async def updatedb(self, ctx):
        self.bot.update_db()

def setup(bot):
    bot.add_cog(Commands(bot))
