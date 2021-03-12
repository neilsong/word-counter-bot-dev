import collections
import re
import discord


def addItem(dict, string, id):
    try:
        if string in dict[str(id)]:
            return False
        dict[str(id)].append(string)
    except:
        dict.update({str(id): [string]})
    return True


def removeItem(dict, string, id):
    state = 0
    try:
        dict[str(id)].remove(string)
        state += 1
        if len(dict[str(id)]) == 0:
            dict.pop(str(id))
            state += 1
    except:
        pass
    return state


def cleanSpecial(string):
    print("\nEmojis")
    emojis = re.findall("<:(?:\S).*:\d{18}>", string)
    if len(emojis):
        for i in emojis:
            print(i)
            string = string.replace(i, "")

    mentions = re.findall("<@!?\d{18}>", string)
    print("\nMentions")
    if len(mentions):
        for i in mentions:
            print(i)
            string = string.replace(i, "")

    rolementions = re.findall("<@&\d{18}>", string)
    print("\nRole Mentions")
    if len(rolementions):
        for i in rolementions:
            print(i)
            string = string.replace(i, "")

    channels = re.findall("<#\d{18}>", string)
    print("\nChannels")
    if len(channels):
        for i in channels:
            print(i)
            string = string.replace(i, "")
    print("\n")
    return (string, emojis + mentions + rolementions + channels)


def splitWords(string):
    string = string.lower()
    words = string.split()
    return words


def cleanTrash(string):
    from main import trashCharacters

    for w in trashCharacters:
        string = string.replace(w, " ")
    return string


async def insert(**kwargs):
    from db import queue

    word = ""
    try:
        word = kwargs["word"]
    except:
        pass
    if word:
        task = (
            kwargs["state"],
            {"id": kwargs["id"], "word": word, "value": kwargs["value"]},
        )
    else:
        task = (kwargs["state"], {"id": kwargs["id"], "value": kwargs["value"]})
    await queue.put(task)


def processTrash(string):
    if string == "":
        return string
    from main import trashCharacters

    for w in trashCharacters:
        if string[0] == w:
            return ""
        string = string.replace(w, " ")
    return string


async def processWord(message, w):
    from main import bot

    if message.guild.id not in bot.serverWords:
        bot.serverWords.update({message.guild.id: {w: 0, "__id": message.guild.id}})
    elif w not in bot.serverWords[message.guild.id]:
        bot.serverWords[message.guild.id].update({w: 0, "__id": message.guild.id})
    bot.serverWords[message.guild.id][w] += 1
    await insert(
        state=4,
        id=message.guild.id,
        word=w,
        value=bot.serverWords[message.guild.id][w],
    )
    if message.author.id not in bot.userWords:
        bot.userWords.update({message.author.id: {w: 0, "__id": message.author.id}})
    elif w not in bot.userWords[message.author.id]:
        bot.userWords[message.author.id].update({w: 0, "__id": message.author.id})
    bot.userWords[message.author.id][w] += 1
    await insert(
        state=3,
        id=message.author.id,
        word=w,
        value=bot.userWords[message.author.id][w],
    )
    if 0 not in bot.serverWords:
        bot.serverWords.update({0: {w: 0, "__id": 0}})
    elif w not in bot.serverWords[0]:
        bot.serverWords[0].update({w: 0, "__id": 0})
    bot.serverWords[0][w] += 1
    await insert(state=4, id=0, word=w, value=bot.serverWords[0][w])


async def processSpecial(message):
    msgcontent = message.content.lower()
    print("\nEmojis")
    emojis = re.findall("<:(?:\S).*:\d{18}>", msgcontent)
    if len(emojis):
        for i in emojis:
            print(i)
            await processWord(message, i)
            msgcontent = msgcontent.replace(i, "")

    mentions = re.findall("<@!?\d{18}>", msgcontent)
    print("\nMentions")
    if len(mentions):
        for i in mentions:
            print(i)
            await processWord(message, i)
            msgcontent = msgcontent.replace(i, "")

    rolementions = re.findall("<@&\d{18}>", msgcontent)
    print("\nRole Mentions")
    if len(rolementions):
        for i in rolementions:
            print(i)
            await processWord(message, i)
            msgcontent = msgcontent.replace(i, "")

    channels = re.findall("<#\d{18}>", msgcontent)
    print("\nChannels")
    if len(channels):
        for i in channels:
            print(i)
            await processWord(message, i)
            msgcontent = msgcontent.replace(i, "")
    print("\n")
    return msgcontent


async def makeEmbed(self, ctx, dict, state, word):
    embeds = []
    count2 = 0
    count = 0
    nD = {}
    for key in dict:
        count2 += 1
        nD[key] = dict[key]
        if count2 % 15 == 0 or count2 == len(dict):
            if not word == "":
                embeds.append(await self.makeEmbed(ctx, nD, count, state, word))
            else:
                embeds.append(await self.makeEmbed(ctx, nD, count, state, ""))
            count += 1

            nD.clear()
    return embeds


async def count(dict, state, ctx, self):
    embeds = []

    words = dict
    words = {
        k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)
    }
    words.pop("__id")
    try:
        for i in self.bot.filter[str(ctx.guild.id)]:
            try:
                words.pop(i)
            except:
                continue
    except:
        pass

    if not len(words):
        return await ctx.send("I haven't logged anything yet.")

    embeds = await makeEmbed(self, ctx, words, state, "")

    return embeds


async def leaderboard(self, ctx, word, isGlobal):
    leaderboard = {}
    if isGlobal == "global":
        for u, c in self.bot.userWords.items():
            try:
                leaderboard.update({u: c[word]})
            except:
                continue
        leaderboard = dict(collections.Counter(leaderboard).most_common(10))
        for u in leaderboard.copy():
            try:
                user = await self.bot.fetch_user(u)
            except:
                leaderboard.pop(u)
                continue
            leaderboard[user] = leaderboard.pop(u)
    else:
        async for user in ctx.guild.fetch_members(limit=None):
            try:
                leaderboard.update({user: self.bot.userWords[user.id][word]})
            except:
                continue
        leaderboard = {
            k: v
            for k, v in sorted(
                leaderboard.items(), key=lambda item: item[1], reverse=True
            )
        }

    if not len(leaderboard):
        return await ctx.send("No one on this server has said this word yet")

    embeds = []
    embeds = await makeEmbed(self, ctx, leaderboard, "top" + isGlobal, word)

    return embeds


async def userfriendlyembed(self, ctx, word):
    word = await userfriendly(self, ctx, word)

    isemoji = testemoji(word)
    if isemoji:
        for c in ["<", ">"]:
            word = word.replace(c, "")
        word = re.sub("\d{18}", "", word, 1)

    return word


async def userfriendly(self, ctx, word):
    ismention = re.search("<@!?\d{18}>", word)
    if ismention:
        for c in ["<", "@", "!", ">"]:
            word = word.replace(c, "")
        try:
            user = await ctx.guild.fetch_member(int(word))
        except:
            user = await self.bot.fetch_user(word)
            return "@" + user.name
        if not user.nick:
            return "@" + user.name
        return "@" + user.nick

    ischannel = re.search("<#\d{18}>", word)
    if ischannel:
        for c in ["<", "#", ">"]:
            word = word.replace(c, "")
        channel = await self.bot.fetch_channel(int(word))
        return "#" + channel.name

    return word


def testemoji(word):
    isemoji = re.search("<:(?:\S).*:\d{18}>", word)
    return isemoji


def find_color(ctx):
    # Find the bot's rendered color. If default color or in a DM, return Discord's grey color

    try:
        if ctx.guild.me.color == discord.Color.default():
            color = discord.Color.greyple()
        else:
            color = ctx.guild.me.color
    except AttributeError:  # * If it's a DM channel
        color = discord.Color.greyple()
    return color


def get_prefix(bot, message):
    from constants import default_prefix

    try:
        return bot.prefixes[str(message.guild.id)]
    except:
        return default_prefix


async def wordListToString(self, ctx, list):
    string = ""
    if len(list) > 1:
        for i in list:
            isemoji = testemoji(i)
            islast = i == list[len(list) - 1]
            i = await userfriendly(self, ctx, i)
            if islast:
                string += (
                    "and "
                    f"{'`' if not isemoji else ''}{i}{'`' if not isemoji else ''}"
                )
            else:
                string += f"{'`' if not isemoji else ''}{i}{'`' if not isemoji else ''}"
                if len(list) > 2:
                    string += ", "
                else:
                    string += " "
    else:
        isemoji = testemoji(list[0])
        string += f"{'`' if not isemoji else ''}{list[0]}{'`' if not isemoji else ''}"
    return string


async def channelListToString(self, ctx, list):
    string = ""
    if len(list) > 1:
        string += "s: "
        first = True
        string += await wordListToString(self, ctx, list)
        for i in range(0, len(string) + int(string.count("`") / 2)):
            if string[i] == "`":
                if first:
                    string = string[:i] + "<#" + string[i + 1 :]
                    first = False
                    i += 1
                else:
                    string = string[:i] + ">" + string[i + 1 :]
                    first = True
    else:
        string += ": " f"<#{list[0]}>"
    return string
