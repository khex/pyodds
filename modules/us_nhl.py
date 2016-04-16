#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("C:/Users/qm69/Code/pyodds/libs")

from mongodb import modules
from mongodb import teams
from mongodb import matches

m_data = dict(
    mhsh="hkusnh",
    sport="hockey",
    country="USA",
    league="NHL",
    odd_url=("hockey", "usa", "nhl")
)

year = ["2015-2016"]

team_dict = [
    dict(tid=113, seasons=year, full="Anaheim Ducks", short="Anaheim", link="anaheim-ducks"),
    dict(tid=114, seasons=year, full="Arizona Coyotes", short="Arizona Coyotes", link="arizona-coyotes"),
    dict(tid=115, seasons=year, full="Boston Bruins", short="Boston", link="boston-bruins"),
    dict(tid=116, seasons=year, full="Buffalo Sabres", short="Buffalo", link="buffalo-sabres"),
    dict(tid=117, seasons=year, full="Calgary Flames", short="Calgary", link="calgary-flames"),
    dict(tid=118, seasons=year, full="Carolina Hurricanes", short="Carolina", link="carolina-hurricanes"),
    dict(tid=119, seasons=year, full="Chicago Blackhawks", short="Chicago", link="chicago-blackhawks"),
    dict(tid=120, seasons=year, full="Colorado Avalanche", short="Colorado", link="colorado-avalanche"),
    dict(tid=121, seasons=year, full="Columbus Blue Jackets", short="Columbus", link="columbus-blue-jackets"),
    dict(tid=122, seasons=year, full="Dallas Stars", short="Dallas", link="dallas-stars"),
    dict(tid=123, seasons=year, full="Detroit Red Wings", short="Detroit", link="detroit-red-wings"),
    dict(tid=124, seasons=year, full="Edmonton Oilers", short="Edmonton", link="edmonton-oilers"),
    dict(tid=125, seasons=year, full="Florida Panthers", short="Florida", link="florida-panthers"),
    dict(tid=126, seasons=year, full="Los Angeles Kings", short="Los Angeles", link="los-angeles-kings"),
    dict(tid=127, seasons=year, full="Minnesota Wild", short="Minnesota", link="minnesota-wild"),
    dict(tid=128, seasons=year, full="Montreal Canadiens", short="Montreal", link="montreal-canadiens"),
    dict(tid=129, seasons=year, full="Nashville Predators", short="Nashville", link="nashville-predators"),
    dict(tid=130, seasons=year, full="New Jersey Devils", short="New Jersey", link="new-jersey-jevils"),
    dict(tid=131, seasons=year, full="New York Islanders", short="NY Islanders", link="new-york-islanders"),
    dict(tid=132, seasons=year, full="New York Rangers", short="NY Rangers", link="new-york-rangers"),
    dict(tid=133, seasons=year, full="Ottawa Senators", short="Ottawa", link="ottawa-senators"),
    dict(tid=114, seasons=year, full="Philadelphia Flyers", short="Philadelphia Flyers", link="philadelphia-flyers"),
    dict(tid=135, seasons=year, full="Pittsburgh Penguins", short="Pittsburgh", link="pittsburgh-penguins"),
    dict(tid=136, seasons=year, full="San Jose Sharks", short="San Jose", link="san-jose-sharks"),
    dict(tid=137, seasons=year, full="St.Louis Blues", short="St.Louis", link="st-louis-blues"),
    dict(tid=138, seasons=year, full="Tampa Bay Lightning", short="Tampa Bay", link="tampa-bay-lightning"),
    dict(tid=139, seasons=year, full="Toronto Maple Leafs", short="Toronto", link="toronto-maple-leafs"),
    dict(tid=140, seasons=year, full="Vancouver Canucks", short="Vancouver", link="vancouver-canucks"),
    dict(tid=141, seasons=year, full="Washington Capitals", short="Washington", link="washington-capitals"),
    dict(tid=142, seasons=year, full="Winnipeg Jets", short="Winnipeg", link="winnipeg-jets")
]

if __name__ == "__main__":
    """
    for t in team_dict:
        t["module"] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
    """
    matches.delete_many('nhl')
