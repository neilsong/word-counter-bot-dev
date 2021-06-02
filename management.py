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
            return await send(ctx, description)
        if len(prefixes) > 1:
            description += "es: "
            description += await wordListToString(self, ctx, prefixes)
        elif len(prefixes) == 1:
            description += ": "
            description += await wordListToString(self, ctx, prefixes)
        await send(ctx, description)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, *, prefixes=""):
        if len(prefixes) > 0:
            prefixlist = prefixes.split(" ")
            self.bot.prefixes.update({str(ctx.guild.id): prefixlist})
            if len(prefixlist) > 1:
                await send(ctx, "Prefixes set")
            else:
                await send(ctx, "Prefix set")
            await insert(state=0, id=str(ctx.guild.id), value=prefixlist)
        else:
            await send(
                ctx,
                "Please set either a one-character prefix, or multiple one-character prefixes separated by spaces",
            )

    @commands.command()
    @commands.guild_only()
    async def blacklist(self, ctx):
        blacklist = "Currently blacklisted channel"
        if not str(ctx.guild.id) in self.bot.blacklist.keys():
            await send(ctx, "There is no blacklist for this server")
            return
        blacklist += await channelListToString(
            self, ctx, self.bot.blacklist[str(ctx.guild.id)]
        )
        await send(ctx, blacklist)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addblacklist(self, ctx, *, channels):
        response = ""
        channels = splitWords(channels)
        if len(channels) > 0:
            for i in channels:
                if not re.search("^<#\d{18}>$", i):
                    response += "Please provide a channel\n"
                    continue
                i = i.replace("<", "").replace("#", "").replace(">", "")
                if addItem(self.bot.blacklist, i, ctx.guild.id):
                    response += f"<#{i}> added\n"
                else:
                    response += f"<#{i}> already blacklisted\n"
            try:
                value = self.bot.blacklist[str(ctx.guild.id)]
                await insert(state=1, id=str(ctx.guild.id), value=value)
            except:
                pass
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces\n"
        await send(ctx, response)

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
                await insert(state=1, id=str(ctx.guild.id), value=value)
            except:
                await self.bot.serverCollection.update_one(
                    {"__id": "blacklist"}, {"$unset": {str(ctx.guild.id): 1}}
                )
        else:
            response += "Please provide either a channel, or multiple channels separated by spaces"
        await send(ctx, response)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def filter(self, ctx):
        filter = "Current filter: "
        if not str(ctx.guild.id) in self.bot.filter.keys():
            await send(ctx, "There is no filter for this server")
            return
        filter += await wordListToString(self, ctx, self.bot.filter[str(ctx.guild.id)])
        await send(ctx, filter)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addfilter(self, ctx, *, words=""):
        stringTuple = cleanSpecial(words)
        words = splitWords(cleanTrash(stringTuple[0]))
        words += stringTuple[1]

        response = ""
        if len(words) > 0:
            for i in words:
                if i in self.bot.defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                if addItem(self.bot.filter, i, ctx.guild.id):
                    if testemoji(i):
                        response += f"{i} added\n"
                    else:
                        ufi = await userfriendly(self, ctx, i)
                        response += f"`{ufi}` added\n"
                else:
                    if testemoji(i):
                        response += f"{i} is already in filter\n"
                    else:
                        ufi = await userfriendly(self, ctx, i)
                        response += f"`{ufi}` is already in filter\n"
            await insert(
                state=2, id=str(ctx.guild.id), value=self.bot.filter[str(ctx.guild.id)]
            )
        else:
            response += (
                "Please add either one word, or multiple words separated by spaces"
            )

        await send(ctx, response)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def removefilter(self, ctx, *, words=""):
        stringTuple = cleanSpecial(words)
        words = splitWords(cleanTrash(stringTuple[0]))
        words += stringTuple[1]

        response = ""
        if len(words) > 0:
            for i in words:
                if i in self.bot.defaultFilter:
                    response += f"`{i}` is in the default filter\n"
                    continue
                state = removeItem(self.bot.filter, i, ctx.guild.id)
                if state > 0:
                    if testemoji(i):
                        response += f"{i} removed\n"
                    else:
                        ufi = await userfriendly(self, ctx, i)
                        response += f"`{ufi}` removed\n"
                    if state > 1:
                        response += f"The filter is now empty\n"
                else:
                    if testemoji(i):
                        response += f"{i} is not in the filter\n"
                    else:
                        ufi = await userfriendly(self, ctx, i)
                        response += f"`{ufi}` is not in the filter\n"
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
        await send(ctx, response)


def setup(bot):
    bot.add_cog(Management(bot))
