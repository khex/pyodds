for (var i = 1; i < 500; i++) {
    try {
        var bookie = globals.getBookmaker(i).getName()
        console.log('    "' + i + '": "' + bookie + '",');
    }
    catch (e) {
       // console.log(i + ': no data')
    }
};


var bokieList = {
    "1": "Interwetten",
    "2": "bwin",
    "3": "bet-at-home",
    "4": "Centrebet",
    "5": "Unibet",
    "7": "Betsson exch.",
    "8": "Stan James",
    "9": "Expekt",
    "10": "PartyBets",
    "11": "Gamebookers",
    "12": "Canbet",
    "14": "10Bet",
    "15": "William Hill",
    "16": "bet365",
    "17": "Blue Square",
    "18": "Pinnacle Sports",
    "19": "Sports Interaction",
    "20": "5Dimes",
    "21": "Betfred",
    "23": "DOXXbet",
    "24": "Betsafe",
    "26": "Betway",
    "27": "888sport",
    "28": "Ladbrokes",
    "29": "Sunmaker",
    "30": "Boylesports",
    "31": "Intertops",
    "32": "Betclic",
    "33": "NordicBet",
    "34": "Bodog",
    "35": "Eurobet",
    "38": "Sportingbet",
    "39": "Betdaq",
    "40": "Sportbet",
    "41": "myBet",
    "43": "Betsson",
    "44": "Betfair",
    "46": "iFortuna.cz",
    "49": "Tipsport.cz",
    "53": "bwin.it",
    "54": "Bet24",
    "55": "Noxwin",
    "56": "188BET",
    "57": "Jetbull",
    "59": "BetUS",
    "60": "Paddy Power",
    "64": "Sports Alive",
    "67": "Internet1x2",
    "68": "BetCRIS",
    "69": "Bookmaker",
    "70": "Tipico",
    "71": "Coral",
    "72": "bets4all",
    "73": "LEON Bets",
    "74": "Skybet",
    "75": "SBOBET",
    "76": "BetVictor",
    "77": "Players Only",
    "78": "BetOnline",
    "79": "BetDSI",
    "80": "12BET",
    "81": "betoto",
    "82": "Heroes Sports",
    "86": "Bet7days",
    "87": "digibet",
    "88": "Legends",
    "89": "Sports-1",
    "90": "Betgun",
    "91": "BetPhoenix",
    "92": "Island Casino",
    "93": "The Greek",
    "97": "Stryyke",
    "98": "Superbahis",
    "99": "World Sports Exchange",
    "100": "Sportsbook",
    "101": "Paf",
    "103": "Redbet",
    "105": "totepool",
    "106": "betChronicle",
    "107": "Betboo",
    "108": "Sports",
    "109": "Oddsmaker",
    "110": "Betonline247",
    "111": "Instant Action Sports",
    "112": "Betinternet",
    "113": "Betcruise",
    "114": "Justbet",
    "115": "Bet770",
    "118": "Extrabet",
    "119": "Goalwin",
    "120": "Circlebet",
    "121": "Titanbet",
    "122": "EurosportBET",
    "123": "Bet911",
    "124": "Luxbet",
    "125": "Bestbet",
    "127": "Bestake",
    "128": "youwin",
    "129": "bwin.fr",
    "130": "Tobet",
    "131": "EurosportBET.fr",
    "132": "SAjOO FR",
    "134": "ParionsWeb.fr",
    "135": "betWize",
    "136": "BetBeast",
    "137": "Bet Victor",
    "138": "BetRedKings",
    "139": "France Pari",
    "140": "Betclic.it",
    "141": "Betclic.fr",
    "142": "Bets10",
    "143": "Sportingbet.au",
    "144": "Partybets.fr",
    "145": "BetVictor.de",
    "146": "AllYouBet",
    "147": "Dafabet",
    "149": "Interwetten.es",
    "150": "LBapuestas",
    "151": "Miapuesta",
    "152": "Triobet",
    "153": "PMU FR",
    "154": "32Red Bet",
    "155": "Totosi",
    "156": "Getwin",
    "157": "Unibet.it",
    "158": "Sportsbet.com.au",
    "159": "Sisal",
    "160": "Unibet.fr",
    "161": "NetBet",
    "162": "STARLOTTOSPORT",
    "163": "iFortuna.pl",
    "164": "iFortuna.sk",
    "165": "STS",
    "166": "Nike",
    "167": "Teletip",
    "168": "Totomix",
    "169": "Tipos",
    "170": "Milenium",
    "171": "Betako",
    "244": "WagerWeb",
    "302": "SBG Global",
    "366": "Victory Tip",
    "367": "Bet1128.it",
    "368": "Globetsport",
    "369": "Admiral",
    "370": "ShilBet",
    "371": "Kajot bet",
    "372": "WilliamHill.it",
    "373": "Top Bet",
    "374": "Interapostas",
    "375": "Interwetten.it",
    "376": "FortunaWin",
    "377": "Bovada",
    "378": "TonyBet",
    "379": "PaddyPower.it",
    "380": "Offsidebet",
    "381": "MarathonBet",
    "382": "Forvetbet",
    "383": "ComeOn",
    "384": "bet-at-home.it",
    "385": "SportsBettingOnline",
    "386": "Ucabet",
    "387": "SportsBetting",
    "388": "90dakika",
    "389": "Heaven Bet",
    "390": "Matchbook",
    "391": "WSBets",
    "392": "bwin.es",
    "393": "Oddsring",
    "394": "Tipico.it",
    "395": "Tempobet",
    "396": "Oddset",
    "397": "Winlinebet",
    "398": "NetBet.fr",
    "399": "Winner",
    "400": "HiperBet",
    "401": "MyBet.it",
    "402": "Hepsibahis",
    "403": "Betrally",
    "404": "Seaniemac",
    "405": "Bet9",
    "406": "Sportium",
    "407": "Vistabet.gr",
    "408": "Sportingbet.gr",
    "409": "Stoiximan",
    "410": "Dhoze",
    "411": "Tipsport.sk",
    "412": "BET2BE",
    "413": "GoBetGo",
    "414": "SAZKAbet",
    "415": "Dashbet",
    "416": "18bet",
    "417": "1xbet",
    "418": "Vernons",
    "419": "bet365.it",
    "420": "WonOdds",
    "421": "Betadonis",
    "422": "5plusbet",
    "423": "NetBet.it",
    "424": "138",
    "425": "Realdealbet"
}