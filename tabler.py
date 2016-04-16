 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Odds portal scraper

Usage:
    statist.py <league> <teams>
    statist.py -d | --debug
    statist.py -v | --version
    statist.py -h | --help

Options:
    -d --debug          Show debug messages.
    -h --help           Show this screen.
    -v --version        Show version.
"""

from docopt import docopt
from termcolor import colored
from termcolor import cprint
from pymongo import MongoClient


MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

args = docopt(__doc__, version='0.0.1')
league = args['<league>']

# home_team, away_team = args['<teams>'].split(' - ')
team_list = args['<teams>'].split(' - ')
home_team, away_team = team_list


def painter(spot, match):
    """
    Возвращает подкрашеную строку текста.

    :param spot: 'home' or 'away'
    :param match: Match data Dictionary
    :return: returns string
    """
    line = match[spot]['ftot']['delta'][0]
    hand = match[spot]['ftot']['delta'][1]
    totl = match[spot]['ftot']['delta'][2]
    itot = match[spot]['ftot']['delta'][3]

    tmpl = '{:>4} {:>5} {:<14} {:<14} {:<14} {:<14}'
    text = tmpl.format(
        match['date']['date'],
        spot,
        # добавить белый для 0.5 и -0.5
        colored(' ' + str(line) if line > 0 else str(line), 'magenta' if line > 0 else 'red'),
        colored(' ' + str(hand) if hand > 0 else str(hand), 'magenta' if hand > 0 else 'red'),
        colored(' ' + str(totl) if totl > 0 else str(totl), 'magenta' if totl > 0 else 'red'),
        colored(' ' + str(itot) if itot > 0 else str(itot), 'magenta' if itot > 0 else 'red'))

    return(text)


def monger(tean_name):
    """
    Get match data from database.

    :param tean_name: ex. 'Seattle Mariners'
    :return: returns string
    """
    team_dict = [{'home.team': tean_name}, {'away.team': tean_name}]
    query = {'league': league, 'seas_type': 'season', '$or': team_dict}
    match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(12)
    return list(match_list)

home_list = monger(home_team)
away_list = monger(away_team)
longest = max(len(home_list), len(away_list))
cprint(' {:^45}|{:^44}'.format(home_team, away_team), 'blue', 'on_white')

for i in range(longest):
    host_spot = 'home' if home_list[i]['home']['team'] == home_team else 'away'
    gest_spot = 'home' if away_list[i]['home']['team'] == away_team else 'away'
    host_text = painter(host_spot, home_list[i])
    gest_text = painter(gest_spot, away_list[i])
    line_tmpl = '  {}. {} | {}. {}'.format(i + 1, host_text, i + 1, gest_text)
    print(line_tmpl)
