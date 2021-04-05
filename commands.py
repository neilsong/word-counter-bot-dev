from discord import channel, message
from discord.ext import commands
import discord

import datetime
import sys
import re
from disputils.pagination import BotEmbedPaginator

from decorator import *
from utilities import *
from constants import *
from main import *
import aiohttp


class Commands(commands.Cog):
    # Commands for the Word Counter Bot

    def __init__(self, bot):
        self.bot = bot

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
            word = await userfriendlyembed(self, ctx, word)
            embed.set_author(
                name=f'Top Users of "{word}" in {ctx.guild.name}',
                icon_url=ctx.guild.icon_url,
            )
        elif user == "topglobal":
            word = await userfriendlyembed(self, ctx, word)
            embed.set_author(
                name=f'Top {str(len(words)) + " " if len(words) > 1 else ""}User{"s" if len(words) > 1 else ""} of "{word}"'
            )
        else:
            embed.set_author(
                name=f"{user.name}'s Most Common Words", icon_url=user.avatar_url
            )

        embed.set_footer(
            text="These listings are accurate as of ", icon_url=self.bot.user.avatar_url
        )
        return embed

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
    async def top(self, ctx, *, word: str = None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        if word == None:
            return await ctx.send(
                f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}top lol`"
            )
        if word in defaultFilter:
            return await ctx.send("That word is filtered by default")
        try:
            if word in self.bot.filter[str(ctx.guild.id)]:
                return await ctx.send("That word is filtered")
        except:
            pass
        # Emote space tester
        if " " in word:
            hasemote = False
            hasmultiple = False
            from constants import emotes

            for i in emotes:
                if i == word:
                    if hasemote:
                        hasmultiple = True
                    else:
                        hasemote = True
            if hasmultiple:
                return await ctx.send(
                    f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}top lol`"
                )
            elif not hasemote:
                words = word.split()
                if words[1] == "global":
                    return await ctx.send(
                        f"If you are trying to get the global leaderboard, do `{get_prefix(self.bot, ctx.message)[0]}topglobal lol`"
                    )
                else:
                    return await ctx.send(
                        f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}top lol`"
                    )

        word = word.lower()
        await ctx.channel.trigger_typing()

        embeds = 0
        embeds = await leaderboard(self, ctx, word, "")

        if isinstance(embeds, list):
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

    @commands.command(aliases=["leaderboardglobal", "highglobal"])
    @commands.guild_only()
    async def topglobal(self, ctx, *, word: str = None):
        # See the leaderboard of the top users of this server for this word. Do `top global` to see the top users across all servers
        # Note: If a user said any words on another server that this bot is also on, those will be taken into account
        if word == None:
            return await ctx.send(
                f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}topglobal lol`"
            )
        if word in defaultFilter:
            return await ctx.send("That word is filtered by default")
        try:
            if word in self.bot.filter[str(ctx.guild.id)]:
                return await ctx.send("That word is filtered")
        except:
            pass
        if " " in word:
            hasemote = False
            hasmultiple = False
            from constants import emotes

            for i in emotes:
                if i == word:
                    if hasemote:
                        hasmultiple = True
                    else:
                        hasemote = True
            if hasmultiple:
                return await ctx.send(
                    f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}topglobal lol`"
                )
            elif not hasemote:
                words = word.split()
                if words[1] == "global":
                    return await ctx.send(
                        f"If you are trying to get the global leaderboard, do `{get_prefix(self.bot, ctx.message)[0]}topglobal lol`"
                    )
                else:
                    return await ctx.send(
                        f"Please type a word or individual emote to search for. Ex: `{get_prefix(self.bot, ctx.message)[0]}topglobal lol`"
                    )

        word = word.lower()
        await ctx.channel.trigger_typing()

        embeds = 0
        embeds = await leaderboard(self, ctx, word, "global")

        if isinstance(embeds, list):
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    # AI Commands

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def readhistory(self, ctx):
        aRead = False
        try:
            aRead = self.bot.readHistory[str(ctx.guild.id)]
        except:
            pass
        if not aRead:
            path = os.path.join(
                os.path.abspath(os.getcwd()), "serverdump", str(ctx.guild.id) + ".txt"
            )
            with codecs.open(path, "w+", "utf-8") as f:

                for channel in ctx.guild.text_channels:
                    print(channel.name)
                    if isbotchannel(str(channel.name).lower()) or isbotchannel(
                        str(channel.category).lower()
                    ):
                        continue
                    channelmessages = await channel.history(limit=99999999999).flatten()
                    for i in range(len(channelmessages)):
                        msg = channelmessages[i]
                        msgcontent = msg.content.replace("\n", " ")

                        if (
                            not msgcontent
                            or msg.author.bot
                            or isbotcommand(i, channelmessages)
                        ):
                            continue

                        f.write(str(msg.author.id) + msgcontent + "\n")
                        await updateWord(msg)

            self.bot.readHistory[str(ctx.guild.id)] = True

            await insert(state=5, id=str(ctx.guild.id), value=True)

            print("done")
        else:
            await ctx.send(
                "History already read. `readhistory` is only allowed once per server."
            )

    @commands.command()
    @isaBotAdmin()
    async def serverdump(self, ctx):
        path = os.path.join(
            os.path.abspath(os.getcwd()), "serverdump", str(ctx.guild.id) + ".txt"
        )

        with codecs.open(path, "w+", "utf-8") as f:

            for channel in ctx.guild.text_channels:
                print(channel.name)
                if isbotchannel(str(channel.name).lower()) or isbotchannel(
                    str(channel.category).lower()
                ):
                    continue
                channelmessages = await channel.history(limit=99999999999).flatten()
                for i in range(len(channelmessages)):
                    msg = channelmessages[i]
                    msgcontent = msg.content.replace("\n", " ")

                    if (
                        not msgcontent
                        or msg.author.bot
                        or isbotcommand(i, channelmessages)
                    ):
                        continue

                    f.write(str(msg.author.id) + msgcontent + "\n")

        await ctx.send("done")

    @commands.command(hidden=True)
    async def setBackend(self, ctx, url=None):
        if not ".ngrok.io" in url:
            return await ctx.send("Invalid URL.")
        global custombackendURL
        session = aiohttp.ClientSession()
        custombackendURL = url
        async with session.get(url) as res:
            r = res.text()
            if ".ngrok.io not found" in r:
                await ctx.send(
                    "Backend set to `" + url + "`, but backend failed to respond."
                )
                custombackendURL = ""
            else:
                await ctx.send("Backend set to `" + url + "`. Backend responsive.")
        await session.close()

    @commands.command()
    async def talk(self, ctx, word=None):
        global rep
        gep = {}
        for r in rep:
            gep[r[:3]] = r
        if not word == None:
            session = aiohttp.ClientSession()
            message = await ctx.send(
                "Your request is being processed, this will take around 45 seconds. (Around 1.5 minutes on cold start)",
                allowed_mentions=discord.AllowedMentions.none(),
            )
            await ctx.channel.trigger_typing()
            URL = ""

            customalive = False

            if custombackendURL:
                async with session.get(custombackendURL) as r:
                    URL = custombackendURL
                    response = await r.text()
                    try:
                        if "GPT" in response:
                            customalive = True
                    except:
                        pass

            backendalive = False

            if not customalive:
                async with session.get(backendURL) as r:
                    URL = backendURL
                    errmsg = "Cloud Run Endpoint is offline - using backup cluster. This might take a while (~2.5 min)"
                    response = await r.text()
                    try:
                        if not "GPT" in response:
                            await message.edit(content=errmsg)
                        else:
                            backendalive = True
                    except:
                        await message.edit(content=errmsg)

            backupalive = False

            if not backendalive:
                async with session.get(backupURL) as r:
                    URL = backupURL
                    errmsg = "Text generation backend offline or invalid. **Follow the instructions here to activate the !talk command:**\n `https://colab.research.google.com/drive/1kHkTNKqObPwNCIx4Gtb_Jk7-EO4tthD-`"
                    response = await r.text()
                    try:
                        if not "GPT" in response:
                            await message.edit(content=errmsg)
                        else:
                            backupalive = True
                    except:
                        await message.edit(content=errmsg)

            alive = backupalive or backendalive or customalive

            if alive:
                URL += "generate" if URL[-1] == "/" else "/" + "generate"
                inputtxt = str(ctx.author.id)[:3] + ctx.message.content[len("!talk ") :]
                r = ""
                if backupalive:
                    from config import AUTH_KEY

                    params = [("input", inputtxt), ("auth", AUTH_KEY)]
                    async with session.get(URL, params=params) as res:
                        r = await res.text()
                else:
                    params = [("input", inputtxt)]
                    async with session.get(URL, params=params) as res:
                        r = await res.text()
                ans = r
                if (
                    "The server returned an invalid or incomplete HTTP response."
                    not in ans
                ):
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
                    await message.edit(
                        "Backend may have shut down during your request."
                    )
            await session.close()
        else:
            await ctx.send("Needs input text. ex:`!talk hello world`")


def setup(bot):
    bot.add_cog(Commands(bot))
