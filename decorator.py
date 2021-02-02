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
    from main import bot
    def predicate(ctx):
        try:
            if ctx.message.channel.id in bot.blacklist[str(ctx.guild.id)]:
                raise commands.DisabledCommand
            else: return True
        except: return True
    return commands.check(predicate)