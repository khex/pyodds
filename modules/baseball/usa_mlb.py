#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.expanduser('../libs/db.py')))

from db import team_insert

sport = "baseball"
country = "usa"
league = "mlb"
long_seas = False  # ???

# nba = ['2013-2014', '2014-2015', ...]
# first element is this season
year = ['2015', '2014', '2013', '2012', '2011',
        '2010', '2009', '2008', '2007', '2006']
team = (
    # opid is oddsportal ID -> http://www.oddsportal.com/search/:lfZXonNq
    dict(tid=1, opid="xAO4gBas", full="Atlanta Hawks",
         short="atlanta-hawks"),
    dict(tid=2, opid="KYD9hVEm", full="Boston Celtics",
         short="boston-celtics"),
    dict(tid=3, opid="bsAMUpDO", full="Brooklyn Nets",
         short="brooklyn-nets"),
    dict(tid=4, opid="", full="Charlotte Hornets",
         short="charlotte-hornets"),
    dict(tid=5, opid="bPjc49q0", full="Chicago Bulls",
         short="chicago-bulls"),
    dict(tid=6, opid="xGk13Tb6", full="Cleveland Cavaliers",
         short="cleveland-cavaliers"),
    dict(tid=7, opid="YouS3mEC", full="Dallas Mavericks",
         short="dallas-mavericks"),
    dict(tid=8, opid="CxvW27TI", full="Denver Nuggets",
         short="denver-nuggets"),
    dict(tid=9, opid="UcjMRj6J", full="Detroit Pistons",
         short="detroit-pistons"),
    dict(tid=10, opid="SxUtXqch", full="Golden State Warriors",
         short="golden-state-warriors"),
    dict(tid=11, opid="lfZXonNq", full="Houston Astros",
         short="houston-astros"),
    dict(tid=12, opid="YPohMUTt", full="Indiana Pacers",
         short="indiana-pacers"),
    dict(tid=13, opid="vPeTYlqm", full="Los Angeles Clippers",
         short="los-angeles-clippers"),
    dict(tid=14, opid="ngegZ8bg", full="Los Angeles Lakers",
         short="los-angeles-lakers"),
    dict(tid=15, opid="U1I5YSDa", full="Memphis Grizzlies",
         short="memphis-grizzlies"),
    dict(tid=16, opid="CQ7AXnT5", full="Miami Heat", short="miami-heat"),
    dict(tid=17, opid="QTBEW6rC", full="Milwaukee Bucks",
         short="milwaukee-bucks"),
    dict(tid=18, opid="KjBIVQcI", full="Minnesota Timberwolves",
         short="minnesota-timberwolves"),
    dict(tid=19, opid="U3yc9SkP", full="New Orleans Pelicans",
         short="new-orleans-pelicans"),
    dict(tid=20, opid="WCNO4nbt", full="New York Knicks",
         short="new-york-knicks"),
    dict(tid=21, opid="0fHFHEWD", full="Oklahoma City Thunder",
         short="oklahoma-city-thunder"),
    dict(tid=22, opid="QZMS36Dn", full="Orlando Magic",
         short="orlando-magic"),
    dict(tid=23, opid="vwRW2QSh", full="Philadelphia 76ers",
         short="philadelphia-76ers"),
    dict(tid=24, opid="M1Gy2pra", full="Phoenix Suns",
         short="phoenix-suns"),
    dict(tid=25, opid="4Awl14c5", full="Portland Trail Blazers",
         short="portland-trail-blazers"),
    dict(tid=26, opid="CvwE1OCB", full="Sacramento Kings",
         short="sacramento-kings"),
    dict(tid=27, opid="IwmkErSH", full="San Antonio Spurs",
         short="san-antonio-spurs"),
    dict(tid=28, opid="CxtbCMdU", full="Toronto Raptors",
         short="toronto-raptors"),
    dict(tid=29, opid="hGuCX5Su", full="Utah Jazz",
         short="utah-jazz"),
    dict(tid=30, opid="W6vGWPsn", full="Washington Wizards",
         short="washington-wizards")
)

for t in team:
    t["sport"] = "baseball"
    t["country"] = "usa"
    t["league"] = "mlb"
    t["seasons"] = year


if __name__ == '__main__':
    team_insert(team)
