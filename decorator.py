from discord.ext import commands
import discord

def isaBotAdmin():
    from config import ADMINS
    def predicate(ctx):
        if not str(ctx.author.id) in ADMINS:
            raise commands.NotOwner()
        return True
    return commands.check(predicate)