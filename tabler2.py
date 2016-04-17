 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Odds portal scraper

Usage:
    statist.py <league>
    statist.py -v | --version
    statist.py -h | --help

Options:
    -h --help       Show this screen.
    -v --version    Show version.
    <league>        Some text.
"""

from docopt import docopt
from termcolor import colored
from termcolor import cprint
from pymongo import MongoClient
from libs.tabler import get_next


MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

args = docopt(__doc__, version='0.3.1')
league = args['<league>']

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

    tmpl = '{:>4} {:>5} {:>14} {:>14} {:>14} {:>14}'
    text = tmpl.format(
        match['date']['date'],
        spot,
        colored(line, 'magenta' if line > 1 else 'red' if line < -1 else 'white'),
        colored(hand, 'magenta' if hand > 0 else 'red'),
        colored(totl, 'magenta' if totl > 0 else 'red'),
        colored(itot, 'magenta' if itot > 0 else 'red'))

    return(text)


def monger(tean_name, spot):
    """
    Get match data from database.

    :param tean_name: ex. 'Seattle Mariners'
    :return: returns string
    """
    if spot == 'ever':
        team_dict = [{'home.team': tean_name}, {'away.team': tean_name}]
        query = {'league': league, 'seas_type': 'season', '$or': team_dict}
    else:
        quer = 'home.team' if spot == 'home' else 'away.team'
        query = {'league': league, 'seas_type': 'season', quer: tean_name}

    match_list = db.matches.find(query).sort([('date.iso', -1)]).limit(12)
    return list(match_list)        


next_team_list = get_next()
for teams in next_team_list:
    print('\n')
    home_team, away_team = teams.split(' - ')

    """ Ever and EVER """
    home_list, away_list = monger(home_team, 'ever'), monger(away_team, 'ever')
    longest = max(len(home_list), len(away_list))
    cprint(' {:^47}|{:^47}'.format(home_team, away_team), 'blue', 'on_white')

    for i in range(longest):
        try:
            host_spot = 'home' if home_list[i]['home']['team'] == home_team else 'away'
            host_text = painter(host_spot, home_list[i])
        except:
            host_text = ' ' * 45

        try:
            gest_spot = 'home' if away_list[i]['home']['team'] == away_team else 'away'
            gest_text = painter(gest_spot, away_list[i])
        except:
            gest_text = ' ' * 45

        line_tmpl = '  {:>2}. {}  | {:>2}. {}'.format(i + 1, host_text, i + 1, gest_text)
        print(line_tmpl)


    """ HOME and AWAY """
    host_list, gest_list = monger(home_team, 'home'),  monger(away_team, 'away')
    longest = max(len(host_list), len(gest_list))
    cprint(' {:^47}|{:^47}'.format(home_team, away_team), 'blue', 'on_white')

    for i in range(longest):
        try:
            host_text = painter('home', host_list[i])
        except:
            host_text = ' ' * 45

        try:
            gest_text = painter('away', gest_list[i])
        except:
            gest_text = ' ' * 45

        line_tmpl = '  {:>2}. {}  | {:>2}. {}'.format(i + 1, host_text, i + 1, gest_text)
        print(line_tmpl)

