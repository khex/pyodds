#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/qm69/Code/delta_odds/libs')

from mdb import modules
from mdb import teams

m_data = dict(mhsh="bsusml", sport="baseball", country="USA",
              league="MLB", odd_url=("baseball", "usa", "mlb"))

year = ['2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005']

team_dict = [
    dict(tid=70, full="Arizona Diamondbacks", short="arizona-diamondbacks", seasons=year),
    dict(tid=71, full="Atlanta Braves", short="atlanta-braves", seasons=year),
    dict(tid=72, full="Baltimore Orioles", short="baltimore-orioles", seasons=year),
    dict(tid=73, full="Boston Red Sox", short="boston-red-sox", seasons=year),
    dict(tid=74, full="Chicago Cubs", short="chicago-cubs", seasons=year),
    dict(tid=75, full="Chicago White Sox", short="chicago-white-sox", seasons=year),
    dict(tid=76, full="Cincinnati Reds", short="cincinnati-reds", seasons=year),
    dict(tid=77, full="Cleveland Indians", short="cleveland-indians", seasons=year),
    dict(tid=78, full="Colorado Rockies", short="colorado-rockies", seasons=year),
    dict(tid=79, full="Detroit Tigers", short="cetroit-tigers", seasons=year),
    dict(tid=80, full="Houston Astros", short="houston-astros", seasons=year),
    dict(tid=81, full="Kansas City Royals", short="kansas-city-royals", seasons=year),
    dict(tid=82, full="Los Angeles Angels", short="los-angeles-angels", seasons=year),
    dict(tid=83, full="Los Angeles Dodgers", short="los-angeles-dodgers", seasons=year),
    dict(tid=84, full="Miami Marlins", short="miami-marlins", seasons=year),
    dict(tid=85, full="Milwaukee Brewers", short="milwaukee-brewers", seasons=year),
    dict(tid=86, full="Minnesota Twins", short="minnesota-twins", seasons=year),
    dict(tid=87, full="New York Mets", short="new-york-mets", seasons=year),
    dict(tid=88, full="New York Yankees", short="new-york-yankees", seasons=year),
    dict(tid=89, full="Oakland Athletics", short="oakland-athletics", seasons=year),
    dict(tid=90, full="Philadelphia Phillies", short="philadelphia-phillies", seasons=year),
    dict(tid=91, full="Pittsburgh Pirates", short="pittsburgh-pirates", seasons=year),
    dict(tid=92, full="San Diego Padres", short="san-diego-padres", seasons=year),
    dict(tid=93, full="San Francisco Giants", short="san-francisco-giants", seasons=year),
    dict(tid=94, full="Seattle Mariners", short="seattle-mariners", seasons=year),
    dict(tid=95, full="St.Louis Cardinals", short="st-louis-cardinals", seasons=year),
    dict(tid=96, full="Tampa Bay Rays", short="tampa-bay-rays", seasons=year),
    dict(tid=97, full="Texas Rangers", short="texas-rangers", seasons=year),
    dict(tid=98, full="Toronto Blue Jays", short="toronto-blue-jays", seasons=year),
    dict(tid=99, full="Washington Nationals", short="washington-nationals", seasons=year),
]

if __name__ == '__main__':

    for t in team_dict:
        t['module'] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
