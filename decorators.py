
from discord.ext import commands, tasks
def isaBotAdmin():
    from main import allowedIds
    def predicate(ctx):
        #print(ctx.author.id )
        if not str(ctx.author.id) in allowedIds:
            raise commands.NotOwner('You do not own this bot.')
        return True
        # a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
    return commands.check(predicate)