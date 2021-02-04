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