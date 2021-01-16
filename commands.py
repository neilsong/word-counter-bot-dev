from discord.ext import commands
import discord

import collections
import datetime
import time
import pprint
import sys


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
    async def about(self, ctx):
        # Some basic info about me

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


    @commands.command()
    async def countS(self, ctx, user: discord.User=None):#,string: discord.=None):
        if user == self.bot.user:
            return await ctx.send("Man, why would I count my own words?")
        if user.bot:
            return await ctx.send("I don't count words said by bots.")
        try:
            words=self.bot.words[user.id]
        except:
            return await ctx.send(f"{user.mention} hasn't said anything that I have logged yet.")
        
        
        await ctx.send("Here's my invite link so I can count words on your server too:\n"
                f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
                "&scope=bot&permissions=8")


    @commands.command()
    async def count(self, ctx, user: discord.User=None):
        """Get the number of times a user has said the N-Word
        Format like this: `count <@mention user>`
        If you don't mention a user, I'll get **your** N-word count
        """
        #for w in message.content:



        if user is None:
            user = ctx.author
        if user == self.bot.user:
            return await ctx.send("Man, why would I count my own words?")
        if user.bot:
            return await ctx.send("I don't count words said by bots.")
        try:
            words=self.bot.words[user.id]
        except:
            return await ctx.send(f"{user.mention} hasn't said anything that I have logged yet.")
        
        counter=0

        words={k: v for k, v in sorted(words.items(), key=lambda item: item[1],reverse=True)}
        for w in words:
            if w=="__id":
                continue
            counter+=words[w]

        embed = discord.Embed(
            title=user.name+"\'s Word Counts",
            description=str(len(words)-1)+
                        " distinct words have been said, "
                        " with "
                        +str(counter)+
                        " words said in total. (Only showing top 10)",
            color=find_color(ctx))
        ct=0
        for w in words:
            if w=="__id":
                continue
            ct+=1
            embed.add_field(name=w, value=str(words[w]), inline=False)
            if ct==10:
                break
        embed.set_footer(text="Note: I don't count words said in the past before I joined this server")
        
        await ctx.send(embed=embed)



    @count.error
    async def count_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument):
            return await ctx.send(exc)

    @commands.command()
    async def invite(self, ctx):
        """Sends an invite link so you can invite me to your own server"""

        await ctx.send("Here's my invite link so I can count N-words on your server too:\n"
                       f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
                       "&scope=bot&permissions=8")

    @commands.command()
    async def stats(self, ctx):
        """View my statistics"""

        await ctx.channel.trigger_typing()

        uptime = datetime.datetime.utcnow() - self.bot.started_at

        #* This code was copied from my other bot, MAT
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

        embed = discord.Embed(
            description=f"User ID: {self.bot.user.id}",
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
            name="Number of Users Who Have Said the N-Word",
            value=f"{len(self.bot.nwords):,}",
            inline=False)
        embed.add_field(
            name="Total N-Words Counted",
            value=f"{self.bot.nwords[0]['total']:,} "
                  f"({self.bot.nwords[0]['hard_r']:,} with hard-R)",
            inline=False)
        embed.set_author(name="N-Word Counter Bot: Statistics", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="These statistics are accurate as of:")

        await ctx.send(embed=embed)

    @commands.command(aliases=["leaderboard", "high"])
    @commands.guild_only()
    async def top(self, ctx, param: str=None):
        """See the leaderboard of the top N-word users of this server. Do `top global` to see the top users across all servers
        Note: If a user said N-words on another server that I'm also on, those will be taken into account
        """
        await ctx.channel.trigger_typing()
        def create_leaderboard():
            leaderboard = {}
            if param == "global":
                for u, n in self.bot.nwords.items():
                    if self.bot.get_user(u):
                        leaderboard.update({self.bot.get_user(u): n["total"]})
                leaderboard = dict(collections.Counter(leaderboard).most_common(10))
            else:
                for m in ctx.guild.members:
                    if m.id in self.bot.nwords and not m.bot:
                        if self.bot.nwords[m.id]["total"]:
                            leaderboard.update({m: self.bot.nwords[m.id]["total"]})
                leaderboard = dict(collections.Counter(leaderboard).most_common(10))
            return leaderboard

        leaderboard = await self.bot.loop.run_in_executor(None, create_leaderboard)
        if not len(leaderboard):
            return await ctx.send("No one on this server has said the N-word yet")

        description = "\n"
        counter = 1
        for m, c in leaderboard.items():
            description += (f"**{counter}.** {m if param == 'global' else m.mention} - __{c:,} "
                            f"time{'' if c == 1 else 's'}__ ({self.bot.nwords[m.id]['hard_r']:,} "
                            "with hard-R)\n")
            counter += 1

        description = description.replace("**1.**", ":first_place:").replace("**2.**", ":second_place:").replace("**3.**", ":third_place:")

        embed = discord.Embed(description=description, color=find_color(ctx),
                              timestamp=datetime.datetime.utcnow())
        if param == "global":
            embed.set_author(
                name=f"Top N-Word Users of All Time")
        else:
            embed.set_author(
                name=f"Top N-Word Users of {ctx.guild.name}", icon_url=ctx.guild.icon_url)

        embed.set_footer(
            text="These listings are accurate as of:", icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @top.error
    async def top_error(self, ctx, exc):
        if isinstance(exc, commands.NoPrivateMessage):
            return await ctx.send(exc)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def edit(self, ctx, user_id: int, total: int, hard_r: int, last_time: int=None):
        """Edit a user's entry in the dict or add a new one"""

        if last_time:
            self.bot.nwords[user_id] = {"id": user_id, "total": total, "hard_r": hard_r, "last_time": last_time}
        else:
            self.bot.nwords[user_id] = {"id": user_id, "total": total, "hard_r": hard_r}
        await ctx.send("Done")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pop(self, ctx, user_id: int):
        """Delete a user's entry from the dict"""

        try:
            self.bot.words.pop(user_id)
            await self.bot.collection.delete_one({"__id": user_id})
            await ctx.send("Done")
        except KeyError as e:
            await ctx.send(f"KeyError: ```{e}```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, query):
        """Execute a query in the database"""

        try:
            with ctx.channel.typing():
                async with self.bot.pool.acquire() as conn:
                    result = await conn.execute(query)
            await ctx.send(f"Query complete:```{result}```")
        except Exception as e:
            await ctx.send(f"Query failed:```{e}```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fetch(self, ctx, *, query):
        """Run a query in the database and fetch the result"""

        try:
            with ctx.channel.typing():
                async with self.bot.pool.acquire() as conn:
                    result = await conn.fetch(query)

            fmtd_result = pprint.pformat([dict(i) for i in result])
            await ctx.send(f"Query complete:```{fmtd_result}```")
        except Exception as e:
            await ctx.send(f"Query failed:```{e}```")

    @commands.command(aliases=["resetstatus"], hidden=True)
    @commands.is_owner()
    async def restartstatus(self, ctx):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
            name=f"for N-Words on {len(self.bot.guilds)} servers",
            type=discord.ActivityType.watching))

        await ctx.send("Reset playing status")

    @commands.command(hidden=True)
    @commands.is_owner()
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
    @commands.is_owner()
    async def updatedb(self, ctx):
        temp = await ctx.send("Manually updating... This may take a few minutes... Please wait...")
        with ctx.channel.typing():
            start = time.perf_counter()
            async with self.bot.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO nwords
                    (id)
                    VALUES {}
                    ON CONFLICT
                        DO NOTHING
                ;""".format(", ".join([f"({u})" for u in self.bot.nwords])))

                for data in self.bot.nwords.copy().values():
                    await conn.execute("""
                        UPDATE nwords
                        SET total = {},
                            hard_r = {}
                        WHERE id = {}
                    ;""".format(data["total"], data["hard_r"], data["id"]))

        delta = time.perf_counter() - start
        mi = int(delta) // 60
        sec = int(delta) % 60
        ms = round(delta * 1000 % 1000)
        await temp.delete()
        await ctx.send(f"Finished updating database ({mi}m {sec}s {ms}ms)")


def setup(bot):
    bot.add_cog(Commands(bot))
