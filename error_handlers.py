from discord.ext import commands
import discord


class Error_Handlers(commands.Cog):
    """Error Handlers for commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        exc = exception
        if isinstance(exc, commands.NotOwner):
            return await ctx.send("You are not an admin of this bot.")

        elif isinstance(exc, commands.NoPrivateMessage):
            return

        elif isinstance(exc, commands.BadArgument):
            return

        elif isinstance(exc, discord.Forbidden):
            return

        elif isinstance(exc, discord.NotFound):
            return

        elif isinstance(exc, commands.CheckFailure):
            return

        elif isinstance(exc, commands.MissingPermissions):
            return await ctx.send("You don't have the permissions to execute this command.")

        else:
            return await ctx.send(
                f"```Command: {ctx.command.qualified_name}\n{exc}```An unknown error occured "
                "and I wasn't able to complete that command. Sorry!")


def setup(bot):
    bot.add_cog(Error_Handlers(bot))
