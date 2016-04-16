#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("C:/Users/qm69/Code/pyodds/libs")

from mongodb import modules
from mongodb import teams

m_data = dict(
    mhsh="bsusml",
    sport="baseball",
    country="USA",
    league="MLB",
    odd_url=("baseball", "usa", "mlb")
)

year = ["2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005"]

team_dict = [
    dict(tid=68, seasons=year, full="National League", short="National", link="national-league"),
    dict(tid=69, seasons=year, full="American League", short="American", link="american-league"),
    dict(tid=70, seasons=year, full="Arizona Diamondbacks", short="Arizona", link="arizona-diamondbacks"),
    dict(tid=71, seasons=year, full="Atlanta Braves", short="Atlanta", link="atlanta-braves"),
    dict(tid=72, seasons=year, full="Baltimore Orioles", short="Baltimore", link="baltimore-orioles"),
    dict(tid=73, seasons=year, full="Boston Red Sox", short="Boston", link="boston-red-sox"),
    dict(tid=74, seasons=year, full="Chicago Cubs", short="Ch Cubs", link="chicago-cubs"),
    dict(tid=75, seasons=year, full="Chicago White Sox", short="Ch White Sox", link="chicago-white-sox"),
    dict(tid=76, seasons=year, full="Cincinnati Reds", short="Cincinnati", link="cincinnati-reds"),
    dict(tid=77, seasons=year, full="Cleveland Indians", short="Cleveland", link="cleveland-indians"),
    dict(tid=78, seasons=year, full="Colorado Rockies", short="Colorado", link="colorado-rockies"),
    dict(tid=79, seasons=year, full="Detroit Tigers", short="Detroit", link="cetroit-tigers"),
    dict(tid=80, seasons=year, full="Houston Astros", short="Houston", link="houston-astros"),
    dict(tid=81, seasons=year, full="Kansas City Royals", short="Kansas", link="kansas-city-royals"),
    dict(tid=82, seasons=year, full="Los Angeles Angels", short="LA Angels", link="los-angeles-angels"),
    dict(tid=83, seasons=year, full="Los Angeles Dodgers", short="LA Dodgers", link="los-angeles-dodgers"),
    dict(tid=84, seasons=year, full="Miami Marlins", short="Miami", link="miami-marlins"),
    dict(tid=85, seasons=year, full="Milwaukee Brewers", short="Milwaukee", link="milwaukee-brewers"),
    dict(tid=86, seasons=year, full="Minnesota Twins", short="Minnesota", link="minnesota-twins"),
    dict(tid=87, seasons=year, full="New York Mets", short="NY Mets", link="new-york-mets"),
    dict(tid=88, seasons=year, full="New York Yankees", short="NY Yankees", link="new-york-yankees"),
    dict(tid=89, seasons=year, full="Oakland Athletics", short="Oakland", link="oakland-athletics"),
    dict(tid=90, seasons=year, full="Philadelphia Phillies", short="Philadelphia", link="philadelphia-phillies"),
    dict(tid=91, seasons=year, full="Pittsburgh Pirates", short="Pittsburgh", link="pittsburgh-pirates"),
    dict(tid=92, seasons=year, full="San Diego Padres", short="San Diego", link="san-diego-padres"),
    dict(tid=93, seasons=year, full="San Francisco Giants", short="San Francisco", link="san-francisco-giants"),
    dict(tid=94, seasons=year, full="Seattle Mariners", short="Seattle", link="seattle-mariners"),
    dict(tid=95, seasons=year, full="St.Louis Cardinals", short="St.Louis", link="st-louis-cardinals"),
    dict(tid=96, seasons=year, full="Tampa Bay Rays", short="Tampa Bay", link="tampa-bay-rays"),
    dict(tid=97, seasons=year, full="Texas Rangers", short="Texas", link="texas-rangers"),
    dict(tid=98, seasons=year, full="Toronto Blue Jays", short="Toronto", link="toronto-blue-jays"),
    dict(tid=99, seasons=year, full="Washington Nationals", short="Washington", link="washington-nationals"),
]

if __name__ == "__main__":

    for t in team_dict:
        t["module"] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
