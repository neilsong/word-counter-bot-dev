from discord.ext import commands
import discord
import datetime
from utilities import wordListToString, find_color
import sys


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):

        cmds = sorted(
            [c for c in self.bot.commands if not c.hidden], key=lambda c: c.name
        )

        description = "I keep track of every word a user says. I'm a pretty simple bot to use. My prefix"
        prefixes = []
        try:
            prefixes = self.bot.prefixes[str(ctx.guild.id)]
        except:
            description += ": `!`"
            await ctx.send(description)
        if len(prefixes) > 1:
            description += "es: "
            description += wordListToString(prefixes)
        elif len(prefixes) == 1:
            description += ": "
            description += wordListToString(prefixes)
        description += "\n\nHere's a short list of my commands:"
        embed = discord.Embed(
            title="Word Counter Bot: Help Command",
            description=description,
            color=find_color(ctx),
        )
        for c in cmds:
            embed.add_field(name=c.name, value=c.help, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        # Some basic info about this bot

        embed = discord.Embed(
            title=str(self.bot.user),
            description=self.bot.app_info.description
            + f"\n\n**User/Client ID**: {self.bot.app_info.id}",
            color=find_color(ctx),
        )

        embed.set_thumbnail(url=self.bot.app_info.icon_url)
        from config import ADMINS

        tadmins = ADMINS.copy()
        sadmins = ''
        for i in range(0, len(tadmins)):
            tadmins[i] = await self.bot.fetch_user(tadmins[i])
            tadmins[i] = f"{tadmins[i].name}#{tadmins[i].discriminator} "
            if i is len(tadmins) - 1:
                tadmins[i] = tadmins[i][:-1]
        embed.add_field(name="Admins", value=tadmins)
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="User Count", value=len(self.bot.users))
        embed.add_field(
            name="Language",
            value=f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
        )
        embed.add_field(
            name="Library", value="[discord.py](https://github.com/Rapptz/discord.py)"
        )
        embed.add_field(name="License", value="MIT")
        embed.add_field(
            name="Source Code",
            value="https://github.com/neilsong/word-counter-bot",
            inline=False,
        )
        embed.add_field(
            name="Contributors", value="https://bit.ly/3cWYlsn", inline=False
        )
        embed.add_field(
            name="Distant Cousin",
            value="https://github.com/NWordCounter/bot",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        # View stats

        await ctx.channel.trigger_typing()

        uptime = datetime.datetime.utcnow() - self.bot.started_at

        y = (
            int(uptime.total_seconds()) // 31557600
        )  # * Number of seconds in 356.25 days
        mo = (
            int(uptime.total_seconds()) // 2592000 % 12
        )  # * Number of seconds in 30 days
        d = int(uptime.total_seconds()) // 86400 % 30  # * Number of seconds in 1 day
        h = int(uptime.total_seconds()) // 3600 % 24  # * Number of seconds in 1 hour
        mi = int(uptime.total_seconds()) // 60 % 60  # * etc.
        se = int(uptime.total_seconds()) % 60

        frmtd_uptime = []
        if y != 0:
            frmtd_uptime.append(f"{y}y")
        if mo != 0:
            frmtd_uptime.append(f"{mo}mo")
        if d != 0:
            frmtd_uptime.append(f"{d}d")
        if h != 0:
            frmtd_uptime.append(f"{h}hr")
        if mi != 0:
            frmtd_uptime.append(f"{mi}m")
        if se != 0:
            frmtd_uptime.append(f"{se}s")

        total = 0
        for i, c in self.bot.serverWords[0].items():
            total += c

        embed = discord.Embed(
            description=f"Bot User ID: {self.bot.user.id}",
            timestamp=datetime.datetime.utcnow(),
            color=find_color(ctx),
        )
        embed.add_field(name="Server Count", value=f"{len(self.bot.guilds):,} servers")
        embed.add_field(
            name="User Count", value=f"{len(self.bot.users):,} unique users"
        )
        embed.add_field(
            name="Channel Count",
            value=f"{len(list(self.bot.get_all_channels()) + self.bot.private_channels):,} "
            "channels",
        )
        embed.add_field(
            name="Memory Usage",
            value=f"{round(self.bot.process.memory_info().rss / 1000000, 2)} MB",
        )
        embed.add_field(
            name="Latency/Ping", value=f"{round(self.bot.latency * 1000, 2)}ms"
        )
        embed.add_field(
            name="Uptime", value=" ".join(frmtd_uptime) + " since last restart"
        )
        embed.add_field(
            name="Number of Users Who Have Said Any Word",
            value=f"{len(self.bot.userWords):,}",
            inline=False,
        )
        embed.add_field(name="Total Words Counted", value=f"{total:,} ", inline=False)
        embed.set_author(
            name="Word Counter Bot: Statistics", icon_url=self.bot.user.avatar_url
        )
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(
            text="These statistics are accurate as of ",
            icon_url=self.bot.user.avatar_url,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        # Sends an invite link

        await ctx.send(
            "Here's my invite link so I can count words on your server too:\n"
            f"https://discordapp.com/oauth2/authorize?client_id={self.bot.app_info.id}"
            "&permissions=67501120&scope=bot"
        )


def setup(bot):
    bot.add_cog(Info(bot))
