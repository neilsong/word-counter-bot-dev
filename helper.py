from discord.ext import commands

def isaBotAdmin():
    from main import allowedIds
    def predicate(ctx):
        if not str(ctx.author.id) in allowedIds:
            raise commands.NotOwner('You are a not an admin of this bot.')
        return True
        # a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
    return commands.check(predicate)