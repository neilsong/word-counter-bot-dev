backendURL = "https://inference-bh4nfikt2a-uc.a.run.app"
custombackendURL = ""
# nltk stopwords + custom words
defaultFilter = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "you're",
    "you've",
    "you'll",
    "you'd",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "she's",
    "her",
    "hers",
    "herself",
    "it",
    "it's",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "that'll",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "don't",
    "should",
    "should've",
    "now",
    "d",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "aren't",
    "couldn",
    "couldn't",
    "didn",
    "didn't",
    "doesn",
    "doesn't",
    "hadn",
    "hadn't",
    "hasn",
    "hasn't",
    "haven",
    "haven't",
    "isn",
    "isn't",
    "ma",
    "mightn",
    "mightn't",
    "mustn",
    "mustn't",
    "needn",
    "needn't",
    "shan",
    "shan't",
    "shouldn",
    "shouldn't",
    "wasn",
    "wasn't",
    "weren",
    "weren't",
    "won",
    "won't",
    "wouldn",
    "wouldn't",
    "u",
    "ur",
    "like",
    "also",
    "oh",
    "js",
    "im",
    "yes",
    "yeah",
    "ye",
    "dont",
    "cant",
    "can't",
    "cannot",
    # top level domains
    "com",
    "org",
    "edu",
    "net",
    "gov",
    "mil",
    "int",
    # hyperlink https & http
    "https:",
    "http:",  # screenshot domain
    "gyazo",
]
trashCharacters = [
    ".",
    "/",
    "\\",
    '"',
    "]",
    "[",
    "|",
    "_",
    "+",
    "{",
    "}",
    ",",
    "= ",
    "*",
    "&",
    "^",
    "~",
    "`",
    "?",
    "$",
    " - ",
    "!",
    "@",
    "#",
    ":",
]
default_prefix = ["!"]
rep = [
    "128148223809080524800",
    "163034309777817600",
    "201427603960233985",
    "208668000763641856",
    "219165083157266433",
    "223194183463075842",
    "244587282206556160",
    "246828256458833921",
    "252199587404709898",
    "264897146837270529",
    "266744140522323977",
    "268865883835727873",
    "276838875878653953",
    "280206031496151040",
    "287396208941465601",
    "294199976802910208",
    "295030935806672897",
    "300648350091575296",
    "302148042461675530",
    "315891984206266369",
    "318105860708630539",
    "321294327277944832",
    "323508930842066945",
    "324239438958034966",
    "326402828958695436",
    "330160837035687936",
    "331559477855780867",
    "336630199078617090",
    "337655303086800907",
    "339961530785202176",
    "340194228502265876",
    "342006129993318400",
    "345399775350358020",
    "349694926214397954",
    "351885110552952834",
    "353115258413383691",
    "354105689372622848",
    "364563157621932053",
    "375665702654443520",
    "378647317022244864",
    "380731057206722560",
    "381854465126432779",
    "383750278912147458",
    "388982968129159168",
    "389251991810867201",
    "392765931757240330",
    "412314043941126150",
    "415232606389534762",
    "423955924336640003",
    "427633830782828545",
    "427976964117364739",
    "428563260170567700",
    "429071485487939618",
    "430562483376488459",
    "432257395352141836",
    "436951249108074496",
    "437091514078724116",
    "438545232271900682",
    "445762512080863285",
    "448314612543127584",
    "450097707034476544",
    "456226577798135808",
    "460884184945262602",
    "466004485614075926",
    "466756929343979543",
    "468109692808331274",
    "471106132727824394",
    "484863754732044288",
    "485957519450177538",
    "495341899637325834",
    "500728343847632907",
    "503037280265568267",
    "503438142607589388",
    "508332604618178561",
    "510477201792040990",
    "511372372004044842",
    "511699378184912911",
    "513194000014901250",
    "515915157512388630",
    "519374820312612867",
    "522608694094200843",
    "523690883934060555",
    "525486921800220674",
    "527638079486558258",
    "528720810936893450",
    "534057317117853696",
    "535539046215057408",
    "542194809025069066",
    "550445940893286400",
    "561622813216210954",
    "562791925183152128",
    "576790674255511570",
    "582992042909761556",
    "583809598671290389",
    "585156637224992788",
    "588482243597565963",
    "589151456045694977",
    "614839022530854916",
    "618259892603584531",
    "619657805166805024",
    "630907530654122004",
    "639191409345167371",
    "641250417568645131",
    "668216780157616139",
    "688174904729927683",
    "690713811312705559",
    "692003785064710224",
    "694398683424227328",
    "696449246097965148",
    "707020401464574012",
    "707094046744772618",
    "708029794054569987",
    "718310331419459595",
    "720139905254031382",
    "723258850769371177",
    "723396894122049566",
    "740087180558598194",
    "740683010256535683",
    "743843989480013945",
    "743915636501119127",
    "750843977065955429",
    "754774923481841744",
    "757264292251697243",
    "762056914313936926",
    "763856934310641737",
    "794993831401488454",
    "801311932333817857",
]
emotes = [
    ":-)",
    ":)",
    ":-]",
    ":]",
    ":-3",
    ":3",
    ":->",
    ":>",
    "8-)",
    "8)",
    ":-}",
    ":}",
    ":o)",
    ":c)",
    ":^) ",
    "=]",
    "=)",
    ":-D",
    ":D",
    "8-D",
    "8D",
    "x-D",
    "xD",
    "X-D",
    "XD",
    "=D",
    "=3",
    "B^D",
    "c:",
    "C:",
    ":-))",
    ":-(",
    ":(",
    ":-c",
    ":c",
    ":-<",
    ":<",
    ":-[",
    ":[",
    ":-||",
    ">:[",
    ":{",
    ":@",
    ":(",
    ";(",
    ":'-(",
    ":'(",
    ":'-)",
    ":')",
    "D-': ",
    "D:<",
    "D:",
    "D8",
    "D;",
    "D= ",
    "DX",
    ":-O",
    ":O",
    ":-o",
    ":o",
    ":-0",
    "8-0",
    ">:O",
    ":-*",
    ":*",
    ":×",
    ";-)",
    ";)",
    "*-)",
    "*)",
    ";-]",
    ";]",
    ";^)",
    ";>",
    ":-,",
    ";D",
    ":-P",
    ":P",
    "X-P",
    "XP",
    "x-p",
    "xp",
    ":-p",
    ":p",
    ":-Þ",
    ":Þ",
    ":-þ",
    ":þ",
    ":-b",
    ":b",
    "d:",
    "=p",
    ">:P",
    ":-/",
    ":/",
    ":-.",
    ">:\\",
    ">:/",
    ":\\",
    "=/",
    "=\\",
    ":L",
    "=L",
    ":S",
    ":-|",
    ":|",
    ":$",
    "://)",
    "://3",
    ":-X",
    ":X",
    ":-#",
    ":#",
    ":-&",
    ":&",
    "O:-)",
    "O:)",
    "0:-3",
    "0:3",
    "0:-)",
    "0:)",
    "0;^)",
    ">:-)",
    ":)",
    "}:-)",
    "}:)",
    "3:-)",
    "3:)",
    ">;)",
    ">:3",
    ";3",
    "|;-)",
    "|-O",
    "B-)",
    ":-J",
    "#-)",
    "%-)",
    "%)",
    ":-###..",
    ":###..",
    "<:-|",
    "',:-|",
    "',:-l",
    ":E",
    "<_<",
    ">_>",
    "</3",
    "<\\3",
    "<3",
    "\\o/",
    "*\\0/*",
    "//0-0\\\\",
    "v.v",
    "O_O",
    "o-o",
    "O_o",
    "o_O",
    "o_o",
    "O-O",
    ">.<",
    "^5",
    "o/\\o",
    ">_>^ ^<_<",
    "V.v.V",
    "V=(° °)=V",
    "( ͡° ͜ʖ ͡°)",
    "(>_<)",
    "(>_<)>",
    "(';')",
    "(^^ゞ",
    "(^_^;)",
    "(-_-;)",
    "(~_~;) ",
    "(・.・;)",
    "(・_・;)",
    "(・・;) ^^;",
    "^_^;",
    "(#^.^#)",
    "(^  ^;)",
    "(^.^)y-.o○",
    "(-.-)y-°°°",
    "(-_-)zzz",
    "(^_-)",
    "(^_-)-☆",
    "((+_+))",
    "(+o+)",
    "(°°)",
    "(°-°)",
    "(°.°)",
    "(°_°)",
    "(°_°>)",
    "(°レ°)",
    "(o|o)",
    "<(｀^´)>",
    "^_^",
    "(°o°)",
    "(^_^)/",
    "(^O^)  ",
    "(^o^)／",
    "(^^)/",
    "(≧∇≦)/",
    "(/◕ヮ◕)/",
    "(^o^)丿",
    "∩(·ω·)∩",
    "(·ω·)",
    "^ω^",
    "(__)",
    "_(._.)_",
    "_(_^_)_",
    "<(_ _)>",
    "<m(__)m>",
    "m(__)m",
    "m(_ _)m",
    "＼(°ロ＼)",
    "(／ロ°)／",
    "('_')",
    "(/_;)",
    "(T_T) (;_;)",
    "(;_;",
    "(;_:)",
    "(;O;)",
    "(:_;)",
    "(ToT)",
    "(Ｔ▽Ｔ)",
    ";_;",
    ";-;",
    ";n;",
    ";;",
    "Q.Q",
    "T.T",
    "TnT",
    "QQ",
    "Q_Q",
    "(ー_ー)!!",
    "(-.-)",
    "(-_-)",
    "(一一)",
    "(；一_一)",
    "(=_=)",
    "(=^・^=)",
    "(=^・・^=)",
    "=^_^=",
    "(..)",
    "(._.)",
    "^m^",
    "(・・?",
    "(?_?)",
    "(－‸ლ)",
    ">^_^<",
    "<^!^>",
    "^/^",
    "（*^_^*）",
    "§^.^§",
    "(^<^)",
    "(^.^)",
    "(^ム^)",
    "(^·^)",
    "(^.^)",
    "(^_^.)",
    "(^_^)",
    "(^^) (^J^)",
    "(*^.^*)",
    "^_^",
    "(#^.^#)",
    "（^—^）",
    "(^^)/~~~",
    "(^_^)/~",
    "(;_;)/~~~",
    "(^.^)/~~~",
    "(-_-)/~~~",
    "($··)/~~~",
    "(@^^)/~~~",
    "(T_T)/~~~",
    "(ToT)/~~~",
    "＼(~o~)／",
    "＼(^o^)／",
    "＼(-o-)／",
    "ヽ(^。^)ノ",
    "ヽ(^o^)丿",
    "(*^0^*)",
    "(*_*)",
    "(*_*;",
    "(+_+)",
    "(@_@)  ",
    "(@_@。",
    "(＠_＠;)",
    "＼(◎o◎)／！",
    "!(^^)!",
    "(*^^)v",
    "(^^)v",
    "(^_^)v",
    "(＾ｖ＾)",
    "(＾▽＾)",
    "(・∀・)",
    "(´∀`)",
    "(⌒▽⌒）",
    "(~o~)",
    "(~_~)",
    "(^^ゞ",
    "(p_-)",
    "((d[-_-]b))",
    '(-"-)',
    "(ーー゛)",
    "(^_^メ)",
    "(-_-メ)",
    "(~_~メ)",
    "(－－〆)",
    "(・へ・)",
    "(｀´)",
    "<`～´>",
    "<`ヘ´>",
    "(ーー;)",
    "(^0_0^)",
    "( ..)φ",
    "φ(..)",
    "(●＾o＾●)",
    "(＾ｖ＾)",
    "(＾ｕ＾)",
    "(＾◇＾)",
    "( ^)o(^ )",
    "(^O^)",
    "(^o^)",
    "(^○^)",
    ")^o^(",
    "(*^▽^*)",
    "(✿◠‿◠)",
    "( ￣ー￣)",
    "(￣□￣;)",
    "°o°",
    "°O°",
    ":O o_O",
    "o_0",
    "o.O",
    "(o.o)",
    "oO",
    "(*´▽｀*)",
    "(*°∀°)=3",
    "（ ﾟ Дﾟ)",
    "(°◇°)",
    "(*￣m￣)",
    "ヽ(´ー｀)┌",
    "¯\\_(ツ)_/¯",
    "(´･ω･`)",
    "(‘A`)",
    "(*^3^)/~☆",
    "uwu",
    "UwU",
    "OwO",
    "OWO",
    "owo",
    ".o○",
    "○o.",
    "( ^^)",
    "_U~~",
    "( ^^)",
    "_旦~~",
    "●～*",
    "￣|○",
    "(╯°□°）╯︵ ┻━┻",
    "┬──┬ ¯\\_(ツ)",
    "┻━┻︵ヽ(`Д´)ﾉ︵ ┻━┻",
    "┬─┬ノ( º _ ºノ) (ノಠ益ಠ)ノ彡┻━┻",
    "m(_ _)m",
    "(`･ω･´)",
    "(｀-´)>",
    "(´；ω；`)",
    "ヽ(´ー｀)ﾉ",
    "ヽ(`Д´)ﾉ",
    "(＃ﾟДﾟ)",
    "（ ´Д｀）",
    "（\u3000ﾟДﾟ）",
    "┐('～`；)┌",
    "（´∀｀）",
    "（\u3000´_ゝ`）",
    "Σ(゜д゜;)",
    "( ﾟヮﾟ)",
    "⊂二二二（＾ω＾）二⊃",
    "(((( ；ﾟДﾟ)))",
    "Σ(ﾟДﾟ)",
    "( ´∀｀)σ)∀`)",
    "( ﾟдﾟ)",
    "(´ー`)y-~~",
    "（ ^_^）o自自o（^_^ ）",
    "m9(・∀・)",
    "ヽ(´ー`)人(´∇｀)人(`Д´)ノ",
    "('A`)",
    "（ ´,_ゝ`)",
    "（´-`）.｡oO( ... )",
    "(ﾟДﾟ;≡;ﾟДﾟ)",
    "( ´д)ﾋｿ(´Д｀)ﾋｿ(Д｀)",
    "（･∀･)つ⑩",
    "⊂（ﾟДﾟ⊂⌒｀つ≡≡≡(´⌒;;;≡≡≡",
    "(ﾟдﾟ)",
    "(ﾟ⊿ﾟ)",
    "щ(ﾟДﾟщ) (屮ﾟДﾟ)屮",
    "（・∀・）",
    "（・Ａ・）",
    "(ﾟ∀ﾟ)",
    "（ つ Д ｀）",
    "エェェ(´д｀)ェェエ",
    "(￣ー￣)",
    "[ﾟдﾟ]",
    "♪┏(・o･)┛♪┗ ( ･o･) ┓",
    "d(*⌒▽⌒*)b",
    "(╬ ಠ益ಠ)",
    "(≧ロ≦)",
    "(ΘεΘ;)",
    "＼| ￣ヘ￣|／＿＿＿＿＿＿＿θ☆( *o*)/",
    "┌(；`～,)┐",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "ヽ(´▽`)/",
    "^ㅂ^",
    "(l'o'l)",
    "ヽ(ｏ`皿′ｏ)ﾉ",
    "(☞ﾟヮﾟ)☞",
    "☜(ﾟヮﾟ☜)",
    "☜(⌒▽⌒)☞",
]

yoMama = [
    "Yo mama is like a hockey player, she only showers after three periods.",
    "Yo mama is like a chicken coop, cocks fly in and out all day.",
    "Yo mama has so many teeth missing, that it looks like her tongue is in jail.",
    "Yo mama's mouth is so big that she speaks in surround sound.",
    "Yo mama is so grouchy that the McDonalds she works in doesn't even serve Happy Meals.",
    "You suck- yo mama does too, but she charges.",
    "Yo mama is like a paper towel, she picks up all kinds of slimy wet stuff.",
    "Yo mama is like Bazooka Joe, 5 cents a blow.",
    "Yo mama is like a telephone, even a 3 year old can pick her up.",
    "Yo mama is like a Christmas tree, everybody hangs balls on her.",
    "Yo mama is like the sun, look at her too long and you'll go blind.",
    "Yo mama is like a library, she's open to the public.",
    "Yo mama is like a fine restaurant, she only takes deliveries in the rear.",
    "Yo mama is like an ATM, open 24 hours.",
    "Yo mama is like a bowling ball- round, heavy, and you can fit three fingers in.",
    "Yo mama is like a basketball hoop, everybody gets a shot.",
    "Yo mama is like a Discover card, she gives cash back.",
    "Yo mama is like a championship ring, everybody puts a finger in her.",
    "Yo mama is like Dominoes Pizza, one call does it all.",
    "Yo mama is like a microwave, press one button and she's hot.",
    "Yo mama is like a mail box, open day and night.",
    "Yo mama is like a bowling ball, she always winds up in the gutter.",
    "Yo mama is like a bus, guys climb on and off her all day long.",
    "Yo mama is like a door knob, everybody gets a turn.",
    "Yo mama is like a light switch, even a little kid can turn her on.",
    "Yo mama's such a ho that 'who's your daddy?' is a multiple-choice question.",
    "You'll never be the man Yo mama was.",
    "Yo mama- 'nuff said.",
    "Yo mama is so lazy that she thinks a two-income family is where 'yo daddy has two jobs.'",
    "Yo mama is so lazy that she's got a remote control just to operate her remote!"
    "Yo mama's arms are so short that she has to tilt her head to scratch her ear.",
    "Yo mama's lips are so big that Chapstick had to invent a spray.",
    "Yo mama is so lazy that she came in last place in a recent snail marathon.",
    "What's the difference between yo momma and a walrus? One has whiskers and smells of fish- the other one is a walrus!"
    "Yo mama is missing a finger and can't count past nine.",
    "Yo mama is so flat that she makes the walls jealous!"
    "Yo mama's gums are so black that she spits Yoo-hoo.",
    "Yo mama is twice the man you are.",
    "Yo mama's head is so small that she got her ear pierced and died.",
    "Yo mama is cross-eyed and watches TV in stereo.",
    "Yo mama is so stupid that she was born on Independence Day and can't remember her birthday.",
    "Yo mama's head is so small that she uses a tea-bag as a pillow.",
    "Yo mama's face is so wrinkled, that she has to screw her hat on.",
    "Yo mama's hips are so big that people set their drinks on them.",
    "Yo mama's hair is so nappy that she has to take Tylenol just to comb it.",
    "Yo mama's feet are so big that her shoes need to have license plates on them!"
    "Yo mama so lonely that she buys hot dogs and nuts wishing she could have sex with them.",
    "Yo mama is so bald that you can see what's on her mind.",
    "Yo mama is like a slaughter house - everybody's hanging their meat up in her.",
    "Yo mama is like a carpenter's dream - flat as a board and easy to nail.",
    "Yo mama is like Humpty Dumpty - First she gets humped, then she gets dumped.",
    "Yo mama is like a bag of potato chips, Free-To-Lay.",
    "Yo mama sweats so much, she creates streams.",
    "Yo mama is like a turtle - once she's on her back she's fucked.",
    "Yo mama is like a fan - she's always blowing someone.",
    "Yo mama is like a goalie - she only changes her pads after three periods.",
    "Yo mama is like a gas station - you gotta pay before you pump!",
    "Yo mama is like Sprint - 10 cents a minute anywhere in the country.",
    "Yo mama smells so bad that the doctor diagnosed her with breath cancer.",
    "Yo mama's breath smells so bad that when she yawns her teeth duck out of the way.",
    "What's the difference between yo mama and a 747? About 20 pounds.",
    "Yo mama's like a shotgun, one cock and she blows.",
    "Yo mama's like the Bermuda Triangle, they both swallow a lot of seamen.",
    "Yo mama's like a 5 foot tall basketball hoop, it ain't that hard to score.",
    "Yo mama's like a vacuum cleaner- she sucks, blows, and then gets laid in the closet.",
    "Yo mama's like the Pillsbury dough boy - everybody pokes her.",
    "Yo mama's like a brick, dirty, flat on both sides, and always getting laid by Mexicans.",
    "Yo mama's like a nickel, she ain't worth a dime.",
    "Yo mama's like a streetlamp, you can find her turned on at night on any street corner.",
    "Yo mama's like a telephone booth, open to the public, costs a quarter, and guys go in and out all day.",
    "Yo mama's like a Reese's Peanut Butter Cup, there's no wrong way to eat her.",
    "Yo mama's like a postage stamp, you lick her, stick her, then send her away.",
    "Yo mama's like a screen door, after a couple of bangs she loosens up.",
    "Yo mama's like a dollar bill, she gets handled all across the country.",
    "Yo mama's like school at 3 o'clock- children keep coming out and nobody can remember all the fathers.",
    "Yo mama's like a bowling ball, she gets picked up, fingered, thrown down the gutter, and she still comes back for more.",
    "Yo mama's like a set of speakers - loud, ugly, lives in a box, and you can turn her up, down, on, and off.",
    "Yo mama's like a birthday cake, everybody gets a piece.",
    "Yo mama's like 7-Eleven - open all night, hot to go, and for 89 cents you can get a slurpy.",
    "Yo mama's like a vacuum cleaner - a real good suck.",
    "Yo mama's like a Snickers bar, packed with nuts.",
    "Yo mama's like a race car driver - she burns a lot of rubbers.",
    "Yo mama's like a parking garage, three bucks and you're in.",
    "Yo mama's like a pool table, she likes balls in her pocket.",
    "Yo mama's got 1 toe & 1 knee and they call her Tony.",
    "Yo mama's got a 4 dollar weave and don't know when to leave.",
    "Yo mama's teeth are so yellow, when she smiles it looks like a Kraft Singles pack.",
    "Yo mama's got Play-Doh teeth.",
    "Yo mama's like the Panama Canal, vessels full of seamen pass through her everyday.",
    "Yo mama likes to applaud, 'cause she's got clap.",
    "Yo mama's got 1 leg longer than the other so they call her call her hip hop.",
    "Yo mama's got more chins than a Chinese phone book.",
    "Yo mama's like a squirrel, she's always got some nuts in her mouth.",
    "Yo mama's like a refrigerator, everyone puts their meat in her.",
    "Yo mama's like a tricycle, she's easy to ride.",
    "Yo mama's like mustard, she spreads easy.",
    "Yo mama's like peanut butter: brown, creamy, and easy to spread.",
    "Yo mama's like McDonalds- Billions and Billions served.",
    "Yo mama's like an elevator, guys go up and down on her all day.",
    "Yo mama's like a railroad track, she gets laid all over the country.",
    "Yo mama's like lettuce, 25 cents a head.",
    "Yo mama's got an eagle's nest wig.",
    "Yo mama's twice the man you are.",
    "Yo mama's got more crust than a bucket of Kentucky Fried Chicken.",
    "Yo mama's got more weave than a dog in traffic.",
    "Yo mama's only got one finger and runs around stealing key rings.",
    "Yo mama's got a peanut butter wig with jelly sideburns.",
    "Yo mama's got a leather wig with suede sideburns.",
    "Yo mama got hit upside the head with an ugly stick.",
    "Yo mama's got so much weave, when a fly goes by her hair swats at it.",
    "Yo mama's so fat, that when she fell, no one was laughing but the ground was cracking up.",
    "Yo mama's so fat she goes to KFC and licks other people's fingers.",
    "Yo mama's so stupid she thinks Taco Bell is a mexican phone company.",
    "Yo mama's so dumb she tried to climb Mountain Dew.",
    "Yo mama's so dumb she went to the dentist to get her Bluetooth fixed.",
    "Yo mama's got no ears and was trying on sunglasses.",
    "Yo mama's got so much weave, AT&T uses her extensions as backup lines.",
    "Yo mama's got so much dandruff, she needs to defrost it before she combs her hair.",
    "Yo mama so bald that I can tell fortunes on her head.",
    "Yo mama so bald that you could draw a line down the middle of her head and it would look like my ass.",
    "Yo mama so bald that when she goes to bed, her head slips off the pillow.",
    "Yo mama so bald that when she braids her hair, it looks like stitches.",
    "Yo mama's breath is so stanky, she eats odour eaters.",
    "Yo mama's got one leg and people call her Ilene.",
    "Yo mama's been on welfare so long that her picture is on food stamps.",
    "Yo mama's like Wal-Mart- She's got different discounts everyday.",
    "Yo mama so hunchbacked, she has to look up to tie her shoes.",
    "Yo mama's nostrils are so huge she makes Patrick Ewing jealous.",
    "Yo mama so hunchbacked, she has to wear goggles to wash dishes.",
    "Yo mama so hunchbacked, she can stand on her feet and her head at the same time.",
    "Yo mama breath so stank, her tooth brush prays every night.",
    "Yo mama's butt hairs are so long, they get clogged in the toilet when she flushes.",
    "Yo mama so hunchbacked, she hits her head on speed bumps.",
]
