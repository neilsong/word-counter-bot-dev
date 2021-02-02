from discord.ext import commands
import discord
def isaBotAdmin():
    from config import ADMINS
    def predicate(ctx):
        if not str(ctx.author.id) in ADMINS:
            raise commands.NotOwner()
        return True
    return commands.check(predicate)



def isAllowed():
    def predicate(ctx):
        if ctx.message.channel.id == 632387107536502797:
            raise commands.DisabledCommand
        return True
    return commands.check(predicate)