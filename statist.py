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
home_team = team_list[0]
away_team = team_list[1]


def colorator(spot, match):
    """ smth about the function """

    line = match[spot]['ftot']['delta'][0]
    hand = match[spot]['ftot']['delta'][1]
    totl = match[spot]['ftot']['delta'][2]
    itot = match[spot]['ftot']['delta'][3]

    tmpl = '{:>4} {:>4} {:<14} {:<14} {:<14} {:<14}'
    text = tmpl.format(
        match['date']['date'],
        spot,
        # добавить белый для 0.5 и -0.5
        colored(' ' + str(line) if line > 0 else str(line), 'magenta' if line > 0 else 'red'),
        colored(' ' + str(hand) if hand > 0 else str(hand), 'magenta' if hand > 0 else 'red'),
        colored(' ' + str(totl) if totl > 0 else str(totl), 'magenta' if totl > 0 else 'red'),
        colored(' ' + str(itot) if itot > 0 else str(itot), 'magenta' if itot > 0 else 'red'))

    print(text)


""" home ever """
team_dict = [{'home.team': home_team}, {'away.team': home_team}]
query = {'league': league, 'seas_type': 'season', '$or': team_dict}
match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(10)

cprint(' {:^40} '.format(home_team), 'blue', 'on_white')
for match in match_list:
    spot = 'home' if match['home']['team'] == home_team else 'away'
    colorator(spot, match)


""" home home """
query = {'league': league, 'seas_type': 'season', 'home.team': away_team}
match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(10)

cprint(' {:^40} '.format(home_team), 'blue', 'on_white')
for match in match_list:
    colorator('home', match)


""" away ever """
team_dict = [{'home.team': away_team}, {'away.team': away_team}]
query = {'league': league, 'seas_type': 'season', '$or': team_dict}
match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(10)

cprint(' {:^40} '.format(away_team), 'blue', 'on_white')
for match in match_list:
    spot = 'home' if match['home']['team'] == away_team else 'away'
    colorator(spot, match)


""" away away """
query = {'league': league, 'seas_type': 'season', 'away.team': away_team}
match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(10)

cprint(' {:^40} '.format(away_team), 'blue', 'on_white')
for match in match_list:
    colorator('away', match)
