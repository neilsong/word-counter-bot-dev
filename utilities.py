from main import trashCharacters
import collections

def wordListToString(list):
    string = ""
    if len(list) > 1:
            for i in list:
                if i == list[len(list)-1]:
                    string += "and " f"`{i}`"
                else: 
                    string += f"`{i}`" 
                    if len(list) > 2:
                        string += ", "
                    else:
                        string += " "
    else:
        string += f"`{list[0]}`"
    return string

def channelListToString(list):
    string = ""
    if len(list) > 1:
            string +="s: "
            first = True
            string += wordListToString(list)
            for i in range(0, len(string) + int(string.count("`")/2)):
                if string[i] == '`':
                    if first:
                        string = string[:i] + "<#" + string[i+1:]
                        first = False
                        i += 1
                    else:
                        string = string[:i] + ">" + string[i+1:]
                        first = True
    else:
        string += ": " f"<#{list[0]}>"
    return string

def addItem(dict, string, id):
    try:
        if string in dict[str(id)]:
            return False
        dict[str(id)].append(string)
    except:
        dict.update({str(id) : [string]})
    return True

def removeItem(dict, string, id):
    state = 0
    try:
        dict[str(id)].remove(string)
        state += 1
        if len(dict[str(id)]) == 0:
            dict.pop(str(id))
            state += 1
    except: pass
    return state

def preprocessWords(string):
    for w in trashCharacters:
        words = string.replace(w, " ")
    words = ' '.join(words.split())
    words = words.lower()
    return words

async def makeEmbed(self, ctx, dict, state, word):
    embeds=[]; count2 = 0; count = 0; nD={}
    for key in dict:
        count2+=1
        nD[key]=dict[key]
        if count2%15==0 or count2==len(dict):
            if not word == "":
                 embeds.append(await self.makeEmbed(ctx,nD,count,state,word))
            else:
                embeds.append(await self.makeEmbed(ctx,nD,count,state, ""))
            count+=1

            nD.clear()
    return embeds

async def count(dict, state, ctx, self):
    embeds=[]

    words = dict
    words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True)}
    words.pop('__id')
    try:
        for i in self.bot.filter[str(ctx.guild.id)]:
            try: words.pop(i)
            except: continue
    except: pass

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
        leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)}
    
    if not len(leaderboard):
        return await ctx.send("No one on this server has said this word yet")
    
    embeds = []
    embeds = await makeEmbed(self, ctx, leaderboard, "top" + isGlobal, word)

    return embeds