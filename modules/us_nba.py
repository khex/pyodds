#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#   path.append("C:/Users/khex/Code/pyodds/libs")
sys.path.append('/home/khex/Code/pyodds/libs')
from mongodb import modules
from mongodb import teams

m_data = dict(
    mhsh="bbusnb",      # unique
    sport="basketball",
    country="USA",
    league="NBA",
    odd_url=("basketball", "usa", "nba")
)

year = [
    '2020-2021',
    '2019-2020',
    '2018-2019',
    '2017-2018',
    '2016-2017',
    '2015-2016',
    '2014-2015',
    '2013-2014',
    '2012-2013',
    '2011-2012',
    '2010-2011',
    '2009-2010',
    '2008-2009',
    '2007-2008',
    '2006-2007',
    '2005-2006'
]

team_dict = [
    dict(tid=1,  opid="xAO4gBas", full="Atlanta Hawks",          short="atlanta-hawks", seasons=year),
    dict(tid=2,  opid="KYD9hVEm", full="Boston Celtics",         short="boston-celtics", seasons=year),
    dict(tid=3,  opid="bsAMUpDO", full="Brooklyn Nets",          short="brooklyn-nets", seasons=year),
    dict(tid=4,  opid="xftMikUg", full="Charlotte Hornets",      short="charlotte-hornets", seasons=year),
    dict(tid=5,  opid="bPjc49q0", full="Chicago Bulls",          short="chicago-bulls", seasons=year),
    dict(tid=6,  opid="xGk13Tb6", full="Cleveland Cavaliers",    short="cleveland-cavaliers", seasons=year),
    dict(tid=7,  opid="YouS3mEC", full="Dallas Mavericks",       short="dallas-mavericks", seasons=year),
    dict(tid=8,  opid="CxvW27TI", full="Denver Nuggets",         short="denver-nuggets", seasons=year),
    dict(tid=9,  opid="UcjMRj6J", full="Detroit Pistons",        short="detroit-pistons", seasons=year),
    dict(tid=10, opid="SxUtXqch", full="Golden State Warriors",  short="golden-state-warriors", seasons=year),
    dict(tid=11, opid="Sr9PQALP", full="Houston Rockets",        short="houston-rockets", seasons=year),
    dict(tid=12, opid="YPohMUTt", full="Indiana Pacers",         short="indiana-pacers", seasons=year),
    dict(tid=13, opid="vPeTYlqm", full="Los Angeles Clippers",   short="los-angeles-clippers", seasons=year),
    dict(tid=14, opid="ngegZ8bg", full="Los Angeles Lakers",     short="los-angeles-lakers", seasons=year),
    dict(tid=15, opid="U1I5YSDa", full="Memphis Grizzlies",      short="memphis-grizzlies", seasons=year),
    dict(tid=16, opid="CQ7AXnT5", full="Miami Heat",             short="miami-heat", seasons=year),
    dict(tid=17, opid="QTBEW6rC", full="Milwaukee Bucks",        short="milwaukee-bucks", seasons=year),
    dict(tid=18, opid="KjBIVQcI", full="Minnesota Timberwolves", short="minnesota-timberwolves", seasons=year),
    dict(tid=19, opid="U3yc9SkP", full="New Orleans Pelicans",   short="new-orleans-pelicans", seasons=year),
    dict(tid=20, opid="WCNO4nbt", full="New York Knicks",        short="new-york-knicks", seasons=year),
    dict(tid=21, opid="0fHFHEWD", full="Oklahoma City Thunder",  short="oklahoma-city-thunder", seasons=year),
    dict(tid=22, opid="QZMS36Dn", full="Orlando Magic",          short="orlando-magic", seasons=year),
    dict(tid=23, opid="vwRW2QSh", full="Philadelphia 76ers",     short="philadelphia-76ers", seasons=year),
    dict(tid=24, opid="M1Gy2pra", full="Phoenix Suns",           short="phoenix-suns", seasons=year),
    dict(tid=25, opid="4Awl14c5", full="Portland Trail Blazers", short="portland-trail-blazers"),
    dict(tid=26, opid="CvwE1OCB", full="Sacramento Kings",       short="sacramento-kings", seasons=year),
    dict(tid=27, opid="IwmkErSH", full="San Antonio Spurs",      short="san-antonio-spurs", seasons=year),
    dict(tid=28, opid="CxtbCMdU", full="Toronto Raptors",        short="toronto-raptors", seasons=year),
    dict(tid=29, opid="hGuCX5Su", full="Utah Jazz",              short="utah-jazz", seasons=year),
    dict(tid=30, opid="W6vGWPsn", full="Washington Wizards",     short="washington-wizards", seasons=year),
    dict(tid=31, opid="zuG9MVqq", full="East",                   short="east", seasons=year),
    dict(tid=32, opid="",         full="West",                   short="West", seasons=year),
    dict(tid=33, opid="dxdenFmO", full="Team World",             short="team-world", seasons=year),
    dict(tid=34, opid="",         full="Team USA",               short="Team-USA", seasons=year),
    dict(tid=66, opid="OzVM8037", full="Team Durant",            short="team-durant", seasons=year),
    dict(tid=67, opid="UP6MJZ7R", full="Team LeBron",            short="team-lebron", seasons=year),
]


if __name__ == '__main__':

    for t in team_dict:
        t['module'] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
