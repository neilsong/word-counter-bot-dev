from discord.ext import commands
import discord
from utilities import *
from decorator import *
import os
import codecs


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        for i in self.bot.defaultFilter:
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
    @isaBotAdmin()
    async def reload(ctx):
        # Reload the bot
        bot.reload_extension("commands")
        bot.reload_extension("error_handlers")
        await ctx.send("Reloaded extensions")

    @commands.command(hidden=True)
    @isaBotAdmin()
    async def restartudb(ctx):
        from db import start_workers, cancel_workers

        await cancel_workers()
        await start_workers()
        await ctx.send("Restarted db workers")

    @commands.command()
    @isaBotAdmin()
    async def serverdump(self, ctx):
        resp = await ctx.send("Dumping Server...")
        path = os.path.join(
            os.path.abspath(os.getcwd()), "serverdump", str(ctx.guild.id) + ".txt"
        )

        with codecs.open(path, "w+", "utf-8") as f:

            for channel in ctx.guild.text_channels:
                print(channel.name, end="")
                if isbotchannel(str(channel.name).lower()) or isbotchannel(
                    str(channel.category).lower()
                ):
                    continue
                try:
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
                    print(" - success")
                except:
                    print(" - error")

        await dataclean(ctx.guild)
        await resp.edit(content="Done\n")


def setup(bot):
    bot.add_cog(Admin(bot))
