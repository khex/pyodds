#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from itertools import groupby
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["delta_test"]

# http://docs.mongodb.org/manual/core/read-operations-introduction/
"""
teams = list(db.teams.find({'$and': [{'tid': {'$gte': 70}}, {'tid': {'$lte': 99}}]},
                           {'full': 1, 'short': 1})
                     .sort('full', 1))
"""


def grouper(arg):
    # k= True or False, t = массив серии
    resp = [list(t)for k, t in groupby(arg, lambda x: x > 0)][0]
    return 1.0 * len(resp) if resp[0] > 0 else -1.0 * len(resp)


def panda(arg1, arg2, league, season, seas_type):
    teams = list(db.teams.find(
            {'$and': [
                {'tid': {'$gte': arg1}},
                {'tid': {'$lte': arg2}}
            ]},
            {'full': 1, 'short': 1})
        .sort('full', 1))
    full_names = [team['full'] for team in teams]
    shot_names = [team['short'] for team in teams]

    ever_list, home_list, away_list = [], [], []
    # game_place = ['Ever', 'Home', 'Away']
    odds_type = ['line', 'hCap', 'totl', 'iTot']

    for name in full_names:
        match_list = db.matches.find({
            'league': league,
            'season': season,
            'seas_type': seas_type,
            '$or': [{'home.team': name},
                    {'away.team': name}]}) \
            .sort([('date.iso', -1)])

        ever, home, away = [[[] for i in range(4)] for r in range(3)]  # 3 x 4
        for match in match_list:

            """   get delta   """
            delta = match["home"]["ftot"]["delta"] if match["home"]["team"] == name else match["away"]["ftot"]["delta"]
            [ever[n].append(delta[n]) for n in range(4)]
            [home[n].append(match["home"]["ftot"]["delta"][n]) for n in range(4) if match["home"]["team"] == name]
            [away[n].append(match["away"]["ftot"]["delta"][n]) for n in range(4) if match["away"]["team"] == name]

        # [-1.0. 2.0, -7.0, 3.0] -> тоесть 30 х 4
        ever_list.append([grouper(ever[i]) for i in range(4)])
        home_list.append([grouper(home[i]) for i in range(4)])
        away_list.append([grouper(away[i]) for i in range(4)])

    ever_df = pd.DataFrame(ever_list, index=shot_names, columns=odds_type)
    home_df = pd.DataFrame(home_list, index=shot_names, columns=odds_type)
    away_df = pd.DataFrame(away_list, index=shot_names, columns=odds_type)

    print(ever_df)
    print(home_df)
    print(away_df)


def place_panda(arg1, arg2, league, season, seas_type):
    teams = list(db.teams.find({'tid': {'$in': arg2}}, {'full': 1, 'short': 1}).sort('full', 1))
    full_names = [team['full'] for team in teams]
    shot_names = [team['short'] for team in teams]

    ever_list, home_list, away_list = [], [], []
    # game_place = ['Ever', 'Home', 'Away']
    odds_type = ['line', 'hCap', 'totl', 'iTot']

    for name in full_names:
        match_list = db.matches.find({
            'league': league,
            'season': season,
            'seas_type': seas_type,
            '$or': [{'home.team': name},
                    {'away.team': name}]}) \
            .sort([('date.iso', -1)])

        ever, home, away = [[[] for i in range(4)] for r in range(3)]  # 3 x 4
        for match in match_list:

            """   get delta   """
            delta = match["home"]["ftot"]["delta"] if match["home"]["team"] == name else match["away"]["ftot"]["delta"]
            [ever[n].append(delta[n]) for n in range(4)]
            [home[n].append(match["home"]["ftot"]["delta"][n]) for n in range(4) if match["home"]["team"] == name]
            [away[n].append(match["away"]["ftot"]["delta"][n]) for n in range(4) if match["away"]["team"] == name]

        # [-1.0. 2.0, -7.0, 3.0] -> тоесть 30 х 4
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
    # panda(100, 112, 'npb', '2015', 'season')
    # panda(70, 99, 'mlb', '2015', 'season')

    hm = [98, 77, 84, 87, 96, 74, 75, 81, 86, 96, 70, 83, 92, 94, 93]
    place_panda('home', hm, 'mlb', '2015', 'season')
    aw = [89, 88, 73, 78, 71, 85, 82, 79, 97, 91, 90, 99, 76, 72, 80]
    place_panda('away', aw, 'mlb', '2015', 'season')

