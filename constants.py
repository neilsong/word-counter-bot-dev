backendURL = ""
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