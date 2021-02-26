from discord import channel, message
from discord.ext import commands
import discord

import datetime
import sys
import re
import requests
from disputils.pagination import BotEmbedPaginator

from main import *
from decorator import *
from utilities import *
from constants import *


class Commands(commands.Cog):
    # Commands for the Word Counter Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):

        cmds = sorted(
            [c for c in self.bot.commands if not c.hidden], key=lambda c: c.name
        )

        description = "I keep track of every word a user says. I'm a pretty simple bot to use. My prefix"
        prefixes = []
        try:
            prefixes = self.bot.prefixes[str(ctx.guild.id)]
        except:
            description += ": `!`"
            await ctx.send(description)
        if len(prefixes) > 1:
            description += "es: "
            description += wordListToString(prefixes)
        elif len(prefixes) == 1:
            description += ": "
            description += wordListToString(prefixes)
        description += "\n\nHere's a short list of my commands:"
        embed = discord.Embed(
            title="Word Counter Bot: Help Command",
            description=description,
            color=find_color(ctx),
        )
        for c in cmds:
            embed.add_field(name=c.name, value=c.help, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        # Some basic info about this bot

        embed = discord.Embed(
            title=str(self.bot.user),
            description=self.bot.app_info.description
            + f"\n\n**User/Client ID**: {self.bot.app_info.id}",
            color=find_color(ctx),
        )

        embed.set_thumbnail(url=self.bot.app_info.icon_url)
        from config import ADMINS

        tadmins = ADMINS.copy()
        for i in range(0, len(tadmins)):
            tadmins[i] = await self.bot.fetch_user(tadmins[i])
        tadmins = wordListToString(tadmins)
        tadmins = tadmins.replace("`", "")
        embed.add_field(name="Admins", value=tadmins)
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="User Count", value=len(self.bot.users))
        embed.add_field(
            name="Language",
            value=f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
        )
        embed.add_field(
            name="Library", value="[discord.py](https://github.com/Rapptz/discord.py)"
        )
        embed.add_field(name="License", value="MIT")
        embed.add_field(
            name="Source Code",
            value="https://github.com/neilsong/word-counter-bot",
            inline=False,
        )
        embed.add_field(
            name="Contributors", value="https://bit.ly/3cWYlsn", inline=False
        )
        embed.add_field(
            name="Distant Cousin",
            value="https://github.com/NWordCounter/bot",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        # View stats

        await ctx.channel.trigger_typing()

        uptime = datetime.datetime.utcnow() - self.bot.started_at

        y = (
            int(uptime.total_seconds()) // 31557600
        )  # * Number of seconds in 356.25 days
        mo = (
            int(uptime.total_seconds()) // 2592000 % 12
        )  # * Number of seconds in 30 days
        d = int(uptime.total_seconds()) // 86400 % 30  # * Number of seconds in 1 day
        h = int(uptime.total_seconds()) // 3600 % 24  # * Number of seconds in 1 hour
        mi = int(uptime.total_seconds()) // 60 % 60  # * etc.
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
            color=find_color(ctx),
        )
        embed.add_field(name="Server Count", value=f"{len(self.bot.guilds):,} servers")
        embed.add_field(
            name="User Count", value=f"{len(self.bot.users):,} unique users"
        )
        embed.add_field(
            name="Channel Count",
            value=f"{len(list(self.bot.get_all_channels()) + self.bot.private_channels):,} "
            "channels",
        )
        embed.add_field(
            name="Memory Usage",
            value=f"{round(self.bot.process.memory_info().rss / 1000000, 2)} MB",
        )
        embed.add_field(
            name="Latency/Ping", value=f"{round(self.bot.latency * 1000, 2)}ms"
        )
        embed.add_field(
            name="Uptime", value=" ".join(frmtd_uptime) + " since last restart"
        )
        embed.add_field(
            name="Number of Users Who Have Said Any Word",
            value=f"{len(self.bot.userWords):,}",
            inline=False,
        )
        embed.add_field(name="Total Words Counted", value=f"{total:,} ", inline=False)
        embed.set_author(
            name="Word Counter Bot: Statistics", icon_url=self.bot.user.avatar_url
        )
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(
            text="These statistics are accurate as of ",
            icon_url=self.bot.user.avatar_url,
        )

        await ctx.send(embed=embed)

    async def makeEmbed(self, ctx, words, pageNum, user, word):

        description = "\n"
        counter = 1
        for m, c in words.items():
            description += (
                f"**{counter+pageNum*15}.** {m.mention if user == 'top' else m} - __{c:,} "
                f"time{'' if c == 1 else 's'}__\n"
            )
            counter += 1

        description = (
            description.replace("**1.**", ":first_place:")
            .replace("**2.**", ":second_place:")
            .replace("**3.**", ":third_place:")
        )

        embed = discord.Embed(
            description=description,
            color=find_color(ctx),
            timestamp=datetime.datetime.utcnow(),
        )

        if user == "server":
            embed.set_author(
                name="The Server's Most Common Words", icon_url=ctx.guild.icon_url
            )
        elif user == "global":
            embed.set_author(name="Global Most Common Words")
        elif user == "top":
            word = await ifmention(self, ctx, word)
            embed.set_author(
                name=f'Top Users of "{word}" in {ctx.guild.name}',
                icon_url=ctx.guild.icon_url,
            )
        elif user == "topglobal":
            word = await ifmention(self, ctx, word)
            embed.set_author(name=f'Top 10 Users of "{word}"')
        else:
            embed.set_author(
                name=f"{user.name}'s Most Common Words", icon_url=user.avatar_url
            )

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url
        )
        return embed

    @commands.command()
    async def invite(self, ctx):
        # Sends an invite link

        await ctx.send(
            "Here's my invite link so I can count words on your server too:\n"
            f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
            "&permissions=67501120&scope=bot"
        )

    @commands.command()
    async def count(
        self,
        ctx,
        user=None,
    ):
        # Get the number of times a user has said any word
        # Format like this: `count <@mention user>`
        # If requester doesn't mention a user, the bot will get requester's count
        # If requester has global as argument, the bot will get the gobal count
        embeds = 0

        await ctx.channel.trigger_typing()

        if user == "server":
            dict = []
            try:
                dict = self.bot.serverWords[ctx.guild.id]
            except:
                return await ctx.send(f"I haven't logged anything in this server yet.")

            embeds = await count(dict, "server", ctx, self)

        elif user == "global":
            dict = []
            try:
                dict = self.bot.serverWords[0]
            except:
                return await ctx.send(f"I haven't logged anything yet.")

            embeds = await count(dict, "global", ctx, self)
        else:
            if not user is None:
                try:
                    user = self.bot.get_user(int(re.sub("[^0-9]", "", user)))
                except:
                    return await ctx.send("Not a valid user.")

            if user is None:
                user = ctx.author
            elif user == self.bot.user:
                return await ctx.send("Man, why would I count my own words?")
            elif user.bot:
                return await ctx.send("I don't count words said by bots.")

            dict = []
            try:
                dict = self.bot.userWords[user.id]
            except:
                return await ctx.send(
                    f"{user.mention} hasn't said anything that I have logged yet."
                )

            embeds = await count(dict, user, ctx, self)

        if isinstance(embeds, list):
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

    @commands.command(aliases=["leaderboard", "high"])
    @commands.guild_only()
    async def top(
        self,
        ctx,
        word: str = None,
        isGlobal: str = "",
    ):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        await ctx.channel.trigger_typing()
        if word == None:
            return await ctx.send(
                f"Please type a word to search for. Ex: `{get_prefix(bot, ctx.message)[0]}top lol`"
            )
        if word in defaultFilter:
            return await ctx.send("That word is filtered by default")
        try:
            if word in self.bot.filter[str(ctx.guild.id)]:
                return await ctx.send("That word is filtered")
        except:
            pass
        if isGlobal and not isGlobal == "global":
            return await ctx.send(
                f"If you are trying to get the global leaderboard, do `{get_prefix(bot, ctx.message)[0]}top lol global`"
            )
        word = word.lower()
        await ctx.channel.trigger_typing()

        embeds = 0
        embeds = await leaderboard(self, ctx, word, isGlobal)

        if isinstance(embeds, list):
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

    # @count.error
    # async def count_error(self, ctx, exc):
    #    if isinstance(exc, commands.BadArgument):
    #        return await ctx.send(exc)

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx):
        description = "My prefix"
        prefixes = []
        try:
            prefixes = self.bot.prefixes[str(ctx.guild.id)]
        except:
            description += ": `!`"
            return await ctx.send(description)
        if len(prefixes) > 1:
            description += "es: "
            description += wordListToString(prefixes)
        elif len(prefixes) == 1:
            description += ": "
            description += wordListToString(prefixes)
        await ctx.send(description)

    @commands.command()
    @commands.guild_only()
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
            await ctx.send(
                "Please set either a one-character prefix, or multiple one-character prefixes separated by spaces"
            )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def removeblacklist(self, ctx, *, channels):
        response = ""
        channels = (
            channels.replace("<", "").replace("#", "").replace(">", "").split(" ")
        )
        if len(channels) > 0:
            for i in channels:
                state = removeItem(self.bot.blacklist, i, ctx.guild.id)
                if state > 0:
                    response += f"<#{i}> removed\n"
                    if state > 1:
                        response += f"The blacklist is now empty\n"
                else:
                    response += f"<#{i}> not blacklisted\n"
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await ctx.send(response)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addblacklist(self, ctx, *, channels):
        response = ""
        channels = (
            channels.replace("<", "").replace("#", "").replace(">", "").split(" ")
        )
        if len(channels) > 0:
            for i in channels:
                if addItem(self.bot.blacklist, i, ctx.guild.id):
                    response += f"<#{i}> added\n"
                else:
                    response += f"<#{i}> already blacklisted\n"

        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await ctx.send(response)

    @commands.command()
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
    @commands.has_permissions(manage_guild=True)
    async def removefilter(self, ctx, *, words=""):
        words = preprocessWords(words)

        response = ""
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                state = removeItem(self.bot.filter, i, ctx.guild.id)
                if state > 0:
                    response += f"`{i}` removed\n"
                    if state > 1:
                        response += f"The filter is now empty\n"
                else:
                    response += f"`{i}` is not in the filter\n"
        else:
            response += (
                "Please remove either one word, or multiple words separated by spaces"
            )

        await ctx.send(response)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addfilter(self, ctx, *, words=""):
        words = preprocessWords(words)

        response = ""
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                if addItem(self.bot.filter, i, ctx.guild.id):
                    response += f"`{i}` added\n"
                else:
                    response += f"`{i}` already in filter\n"
        else:
            response += (
                "Please add either one word, or multiple words separated by spaces"
            )

        await ctx.send(response)

    @commands.command()
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
    async def edituser(self, ctx, user_id: int, word: str = None, count: int = 0):
        # Edit a user's entry in all collections or add a new one
        if not user_id or not word or not count:
            return ctx.send("Parameters: user_id, word, count")

        change = 0
        try:
            change = count - self.bot.userWords[user_id][word]
        except:
            change = count

        if count == 0:
            try:
                self.bot.userWords[user_id].pop(word)
            except:
                pass

        self.bot.userWords[user_id][word] = count
        self.bot.serverWords[ctx.guild.id][word] += change
        self.bot.serverWords[0][word] += change

        await ctx.send("Done")

    @commands.command(hidden=True)
    @isaBotAdmin()
    async def popdefaultfilter(self, ctx):
        await ctx.channel.trigger_typing()
        for i in defaultFilter:
            for u in self.bot.userWords.keys():
                try:
                    self.bot.userWords[u].pop(i)
                except:
                    continue
            for u in self.bot.serverWords.keys():
                try:
                    self.bot.serverWords[u].pop(i)
                except:
                    continue
            try:
                self.bot.serverWords[0].pop(i)
            except:
                pass
            await self.bot.collection.update_many({}, {"$unset": {i: 1}})
        await ctx.send("Done")

    @commands.command(hidden=True)
    @isaBotAdmin()
    async def popword(self, ctx, word: str = None):
        # Pop a word from all collections
        await ctx.channel.trigger_typing()
        for u in self.bot.userWords:
            try:
                self.bot.userWords[u].pop(word)
            except:
                continue
        for u in self.bot.serverWords:
            try:
                self.bot.serverWords[u].pop(word)
            except:
                continue
        try:
            self.bot.serverWords[0].pop(word)
        except:
            pass
        await self.bot.collection.update_many({}, {"$unset": {word: 1}})
        await ctx.send("Done")

    @commands.command(hidden=True)
    @isaBotAdmin()
    @commands.guild_only()
    async def popuser(self, ctx, user_id: int):
        # Pop a user from all collections
        await ctx.channel.trigger_typing()
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
    #
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
    async def restartstatus(self, ctx):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                name=f"any Words on {len(self.bot.guilds)} servers",
                type=discord.ActivityType.watching,
            ),
        )

        await ctx.send("Reset playing status")

    @commands.command(hidden=True)
    @isaBotAdmin()
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
    async def setBackend(self, ctx, url=None):
        if not ".ngrok.io" in url:
            return await ctx.send("Invalid url.")
        global backendURL
        backendURL = url
        if ".ngrok.io not found" in requests.get(url=backendURL).text:
            await ctx.send(
                "Backend set to `" + url + "`, but backend failed to respond."
            )
        else:
            await ctx.send("Backend set to `" + url + "`. Backend responsive.")

    @commands.command()
    async def talk(self, ctx, word=None):
        rep = [
            "128148223809080524800",
            "163034309777817600",
            "201427603960233985",
            "208668000763641856",
            "219165083157266433",
            "223194183463075842",
            "244587282206556160",
            "246828256458833921",
            "252199587404709898",
            "264897146837270529",
            "266744140522323977",
            "268865883835727873",
            "276838875878653953",
            "280206031496151040",
            "287396208941465601",
            "294199976802910208",
            "295030935806672897",
            "300648350091575296",
            "302148042461675530",
            "315891984206266369",
            "318105860708630539",
            "321294327277944832",
            "323508930842066945",
            "324239438958034966",
            "326402828958695436",
            "330160837035687936",
            "331559477855780867",
            "336630199078617090",
            "337655303086800907",
            "339961530785202176",
            "340194228502265876",
            "342006129993318400",
            "345399775350358020",
            "349694926214397954",
            "351885110552952834",
            "353115258413383691",
            "354105689372622848",
            "364563157621932053",
            "375665702654443520",
            "378647317022244864",
            "380731057206722560",
            "381854465126432779",
            "383750278912147458",
            "388982968129159168",
            "389251991810867201",
            "392765931757240330",
            "412314043941126150",
            "415232606389534762",
            "423955924336640003",
            "427633830782828545",
            "427976964117364739",
            "428563260170567700",
            "429071485487939618",
            "430562483376488459",
            "432257395352141836",
            "436951249108074496",
            "437091514078724116",
            "438545232271900682",
            "445762512080863285",
            "448314612543127584",
            "450097707034476544",
            "456226577798135808",
            "460884184945262602",
            "466004485614075926",
            "466756929343979543",
            "468109692808331274",
            "471106132727824394",
            "484863754732044288",
            "485957519450177538",
            "495341899637325834",
            "500728343847632907",
            "503037280265568267",
            "503438142607589388",
            "508332604618178561",
            "510477201792040990",
            "511372372004044842",
            "511699378184912911",
            "513194000014901250",
            "515915157512388630",
            "519374820312612867",
            "522608694094200843",
            "523690883934060555",
            "525486921800220674",
            "527638079486558258",
            "528720810936893450",
            "534057317117853696",
            "535539046215057408",
            "542194809025069066",
            "550445940893286400",
            "561622813216210954",
            "562791925183152128",
            "576790674255511570",
            "582992042909761556",
            "583809598671290389",
            "585156637224992788",
            "588482243597565963",
            "589151456045694977",
            "614839022530854916",
            "618259892603584531",
            "619657805166805024",
            "630907530654122004",
            "639191409345167371",
            "641250417568645131",
            "668216780157616139",
            "688174904729927683",
            "690713811312705559",
            "692003785064710224",
            "694398683424227328",
            "696449246097965148",
            "707020401464574012",
            "707094046744772618",
            "708029794054569987",
            "718310331419459595",
            "720139905254031382",
            "723258850769371177",
            "723396894122049566",
            "740087180558598194",
            "740683010256535683",
            "743843989480013945",
            "743915636501119127",
            "750843977065955429",
            "754774923481841744",
            "757264292251697243",
            "762056914313936926",
            "763856934310641737",
            "794993831401488454",
            "801311932333817857",
        ]
        gep = {}
        for r in rep:
            gep[r[:3]] = r
        if not word == None:
            URL = backendURL
            # check if server is alive
            if ".ngrok.io not found" in requests.get(url=URL).text:
                return await ctx.send(
                    "Text generation backend offline or invalid. Follow the instructions here to start your own backend `https://colab.research.google.com/drive/1kHkTNKqObPwNCIx4Gtb_Jk7-EO4tthD-`"
                )
            URL += "" if URL[:-1] == "/" else "/" + "generate"
            message = await ctx.send(
                "Your request is being processed, this will take around 20 seconds.",
                allowed_mentions=discord.AllowedMentions.none(),
            )
            await ctx.channel.trigger_typing()
            inputtxt = str(ctx.author.id)[:3] + ctx.message.content[len("!talk ") :]
            r = requests.get(url=URL, params={"input": inputtxt})
            ans = r.text
            if "The server returned an invalid or incomplete HTTP response." not in ans:
                ans = ans.split("\n")
                out = []
                for msg in ans:
                    try:
                        out.append("<@" + gep[msg[:3]] + ">" + msg[3:])
                    except:
                        out.append(msg)
                await message.edit(
                    content=("\n".join(out)[:2000]),
                    allowed_mentions=discord.AllowedMentions.none(),
                )
            else:
                await message.edit("Backend may have shut down during your request.")
        else:
            await message.edit("Needs input text. ex:`!talk hello world`")


def setup(bot):
    bot.add_cog(Commands(bot))
