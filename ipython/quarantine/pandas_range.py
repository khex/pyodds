#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from itertools import groupby
from pymongo import MongoClient

URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(URI)
db = client.get_database()


def grouper(arg):
    # k= True or False, t= arry of series
    print(arg)
    resp = [list(t)for k, t in groupby(arg, lambda x: x > 0)][0]
    return 1.0 * len(resp) if resp[0] > 0 else -1.0 * len(resp)


def place_panda(arg1, arg2, leag, seas_year, seas_type):
    teams = list(db.teams.find({'tid': {'$in': arg2}}, {'full': 1, 'short': 1}).sort('full', 1))
    full_names = [team['full'] for team in teams]
    shot_names = [team['short'] for team in teams]

    ever_list, home_list, away_list = [], [], []
    # game_place = ['Ever', 'Home', 'Away']
    odds_type = ['line', 'hCap', 'totl', 'iTot']

    for name in full_names:
        quer = {'league': leag, 'seas_year': seas_year, 'seas_type': seas_type,
                '$or': [{'home.team': name}, {'away.team': name}]}
        match_list = db.matches.find(quer).sort([('date.iso', -1)])
        print(len(list(match_list)))
        ever, home, away = [[[] for i in range(4)] for r in range(3)]  # 3 x 4
        for match in match_list:

            # get deltas
            delta = match["home"]["ftot"]["delta"] if match["home"]["team"] == name else match["away"]["ftot"]["delta"]
            [ever[n].append(delta[n]) for n in range(4)]
            [home[n].append(match["home"]["ftot"]["delta"][n]) for n in range(4) if match["home"]["team"] == name]
            [away[n].append(match["away"]["ftot"]["delta"][n]) for n in range(4) if match["away"]["team"] == name]

        # [-1.0. 2.0, -7.0, 3.0] -> тоесть 30 х 4
            print(ever[i])
        ever_list.append([grouper(ever[i]) for i in range(4)])
        home_list.append([grouper(home[i]) for i in range(4)])
        away_list.append([grouper(away[i]) for i in range(4)])

    ever_df = pd.DataFrame(ever_list, index=shot_names, columns=odds_type)
    home_df = pd.DataFrame(home_list, index=shot_names, columns=odds_type)
    away_df = pd.DataFrame(away_list, index=shot_names, columns=odds_type)

    print(ever_df)
    if arg1 == 'home':
        print(home_df)
    else:
        print(away_df)


if __name__ == '__main__':
    hm = [1, 3, 5, 7, 9]
    place_panda('home', hm, 'nba', '2017-2018', 'season')
    aw = [2, 4, 6, 8, 10]
    place_panda('away', aw, 'nba', '2017-2018', 'season')

