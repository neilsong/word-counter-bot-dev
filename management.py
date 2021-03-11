from discord.ext import commands
import discord
from utilities import *


class Management(commands.Cog):
    # Commands for the Word Counter Bot

    def __init__(self, bot):
        self.bot = bot

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
            await insert(state=0, id=str(ctx.guild.id), value=prefixlist)
        else:
            await ctx.send(
                "Please set either a one-character prefix, or multiple one-character prefixes separated by spaces"
            )

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
            await insert(
                state=1,
                id=str(ctx.guild.id),
                value=self.bot.blacklist[str(ctx.guild.id)],
            )
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await ctx.send(response)

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
            try:
                value = self.bot.blacklist[str(ctx.guild.id)]
                await insert(state=2, id=str(ctx.guild.id), value=value)
            except:
                await self.bot.serverCollection.update_one(
                    {"__id": "blacklist"}, {"$unset": {str(ctx.guild.id): 1}}
                )
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
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

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addfilter(self, ctx, *, words=""):
        words = preprocessWords(words)

        response = ""
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in self.bot.defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                if addItem(self.bot.filter, i, ctx.guild.id):
                    response += f"`{i}` added\n"
                else:
                    response += f"`{i}` already in filter\n"
            await insert(
                state=2, id=str(ctx.guild.id), value=self.bot.filter[str(ctx.guild.id)]
            )
        else:
            response += (
                "Please add either one word, or multiple words separated by spaces"
            )

        await ctx.send(response)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def removefilter(self, ctx, *, words=""):
        words = preprocessWords(words)

        response = ""
        if len(words) > 0:
            wordlist = words.split(" ")
            for i in wordlist:
                if i in self.bot.defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                state = removeItem(self.bot.filter, i, ctx.guild.id)
                if state > 0:
                    response += f"`{i}` removed\n"
                    if state > 1:
                        response += f"The filter is now empty\n"
                else:
                    response += f"`{i}` is not in the filter\n"
            try:
                value = self.bot.filter[str(ctx.guild.id)]
                await insert(state=2, id=str(ctx.guild.id), value=value)
            except:
                await self.bot.serverCollection.update_one(
                    {"__id": "filter"}, {"$unset": {str(ctx.guild.id): 1}}
                )
        else:
            response += (
                "Please remove either one word, or multiple words separated by spaces"
            )
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Management(bot))
