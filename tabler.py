#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Odds portal scraper

Usage:
    tabler.py <league> <teams> [<season>]
    tabler.py -d | --debug
    tabler.py -v | --version
    tabler.py -h | --help

Options:
    python tabler.py nba "Los Angeles Lakers - Phoenix Suns"
    python tabler.py nba "San Antonio Spurs - Utah Jazz" "2017-2018"
    -d --debug          Show debug messages.
    -h --help           Show this screen.
    -v --version        Show version.
"""
import sys
#   path.append('C:/Users/khex/Code/pyodds/libs')
sys.path.append('/home/khex/Code/pyodds/libs')
from docopt import docopt
from termcolor import colored
from termcolor import cprint
from pymongo import MongoClient

""" TODO
      [ ] limit MongoFind by arg params
      [ ] filter MongoDB by season or date $gt: date(1, 1, 2018)
      [ ] add second header line with hCap, Totl, iTot
"""

MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
MONGO_ATLAS = "mongodb+srv://stavros:balalajka7@cluster0.62wbu.mongodb.net/deltabase"

client = MongoClient(MONGO_ATLAS)
db = client.get_default_database()

args = docopt(__doc__, version='0.0.1')
league = args['<league>']
home_team, away_team = args['<teams>'].split(' - ')
season = args['<season>'] or '2020-2021'


def monger(tean_name):
    """ Get matches from database.
        :params tean_name: string  - ex. 'Seattle Mariners'.
        :return match_list: string - list of resalts.
    """
    query = {
        'league': league,
        'seas_type': 'season',
        'seas_year': season,
        '$or': [{'home.team': tean_name}, {'away.team': tean_name}] }
    match_list = db.matches.find(query).sort([('date.ts', -1)])  # .limit(30)
    return list(match_list)


def painter(spot, match):
    """ Color text string.
        :params spot: string - 'home' or 'away'.
        :params match: dict  - match data dictionary.
        :return line: string - colored line for table.
    """
    arry = [match[spot]['ftot']['delta'][n] for n in range(4)]
    # line, hand, totl, itot 
    l, h, t, i = [colored(' ' + str(x) if x > 0 else str(x), 'magenta' if x > 0 else 'red') for x in arry]
    tmpl = '{:<5} {:>5} {:<14} {:<14} {:<14} {:<14}'
    line = tmpl.format(match['date']['date'], spot, l, h, t, i)
    return(line)


def printer(home_arry, away_arry, home_name, away_name):
    """ Print colored lines.
    :params home_arry, away_arry: list - list of games.
    :params home_name, away_name: string - name of the team.
    :params away_arry: list - list of games.
    """
    cprint('{:^47}|{:^47}'.format(home_name, away_name), 'blue', 'on_white')
    # cprint('{:^47}|{:^47}'.format('date', 'hCap'), 'blue', 'on_white')
    shortest = min(len(home_arry), len(away_arry))
    for i in range(shortest):
        host_spot = 'home' if home_arry[i]['home']['team'] == home_team else 'away'
        gest_spot = 'home' if away_arry[i]['home']['team'] == away_team else 'away'

        host_text = painter(host_spot, home_arry[i])
        gest_text = painter(gest_spot, away_arry[i])

        print('  {:>2}. {} | {:>2}. {}'.format(i + 1, host_text, i + 1, gest_text))


"""  Slice 12 games from list  """
home_list = monger(home_team)
away_list = monger(away_team)
printer(home_list, away_list, home_team, away_team)

"""  Filter only home games for home_team & away games for away_team  """
home_mist = list(filter(lambda t: t['home']['team'] == home_team, home_list))
away_mist = list(filter(lambda t: t['away']['team'] == away_team, away_list))
printer(home_mist, away_mist, 'Home', 'Away')
