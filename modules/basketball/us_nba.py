#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/qm69/Code/delta_odds/libs')

from mdb import module
from mdb import team

m_data = {
    "mhsh": "bbusnb",  # unique
    "sport": "basketball",
    "country": "USA",
    "league": "NBA",
    "odd_url": ("basketball", "usa", "nba")
}

year = ['2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
        '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006']

teams = [
    dict(tid=1, opid="xAO4gBas", full="Atlanta Hawks", short="atlanta-hawks", seasons=year),
    dict(tid=2, opid="KYD9hVEm", full="Boston Celtics", short="boston-celtics", seasons=year),
    dict(tid=3, opid="bsAMUpDO", full="Brooklyn Nets", short="brooklyn-nets", seasons=year),
    dict(tid=4, opid="xftMikUg", full="Charlotte Hornets", short="charlotte-hornets", seasons=year),
    dict(tid=5, opid="bPjc49q0", full="Chicago Bulls", short="chicago-bulls", seasons=year),
    dict(tid=6, opid="xGk13Tb6", full="Cleveland Cavaliers", short="cleveland-cavaliers", seasons=year),
    dict(tid=7, opid="YouS3mEC", full="Dallas Mavericks", short="dallas-mavericks", seasons=year),
    dict(tid=8, opid="CxvW27TI", full="Denver Nuggets", short="denver-nuggets", seasons=year),
    dict(tid=9, opid="UcjMRj6J", full="Detroit Pistons", short="detroit-pistons", seasons=year),
    dict(tid=10, opid="SxUtXqch", full="Golden State Warriors", short="golden-state-warriors", seasons=year),
    dict(tid=11, opid="lfZXonNq", full="Houston Astros", short="houston-astros", seasons=year),
    dict(tid=12, opid="YPohMUTt", full="Indiana Pacers", short="indiana-pacers", seasons=year),
    dict(tid=13, opid="vPeTYlqm", full="Los Angeles Clippers", short="los-angeles-clippers", seasons=year),
    dict(tid=14, opid="ngegZ8bg", full="Los Angeles Lakers", short="los-angeles-lakers", seasons=year),
    dict(tid=15, opid="U1I5YSDa", full="Memphis Grizzlies", short="memphis-grizzlies", seasons=year),
    dict(tid=16, opid="CQ7AXnT5", full="Miami Heat", short="miami-heat", seasons=year),
    dict(tid=17, opid="QTBEW6rC", full="Milwaukee Bucks", short="milwaukee-bucks", seasons=year),
    dict(tid=18, opid="KjBIVQcI", full="Minnesota Timberwolves", short="minnesota-timberwolves", seasons=year),
    dict(tid=19, opid="U3yc9SkP", full="New Orleans Pelicans", short="new-orleans-pelicans", seasons=year),
    dict(tid=20, opid="WCNO4nbt", full="New York Knicks", short="new-york-knicks", seasons=year),
    dict(tid=21, opid="0fHFHEWD", full="Oklahoma City Thunder", short="oklahoma-city-thunder", seasons=year),
    dict(tid=22, opid="QZMS36Dn", full="Orlando Magic", short="orlando-magic", seasons=year),
    dict(tid=23, opid="vwRW2QSh", full="Philadelphia 76ers", short="philadelphia-76ers", seasons=year),
    dict(tid=24, opid="M1Gy2pra", full="Phoenix Suns", short="phoenix-suns", seasons=year),
    dict(tid=25, opid="4Awl14c5", full="Portland Trail Blazers", short="portland-trail-blazers"),
    dict(tid=26, opid="CvwE1OCB", full="Sacramento Kings", short="sacramento-kings", seasons=year),
    dict(tid=27, opid="IwmkErSH", full="San Antonio Spurs", short="san-antonio-spurs", seasons=year),
    dict(tid=28, opid="CxtbCMdU", full="Toronto Raptors", short="toronto-raptors", seasons=year),
    dict(tid=29, opid="hGuCX5Su", full="Utah Jazz", short="utah-jazz", seasons=year),
    dict(tid=30, opid="W6vGWPsn", full="Washington Wizards", short="washington-wizards", seasons=year)
]

m_id = module.save(m_data)
print(type(teams))
print(m_id)
resp = team.save(teams, m_id)

for r in resp:
    print(r)
