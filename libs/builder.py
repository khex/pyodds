#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from logger import log_db

nba_teams = [('Atlanta Hawks', 'Atlanta')]
link_names = ['atlanta-hawks', 'boston-celtics']
"""
def get_teams(team_full):
    for team in nba_teams:
        if team_full == team[0]:
            return team
"""


def stat_line(score, line):
    """
    Подсчет результата матча:
        фаворит выиграл: 1
        аутсайдер выиграл: 2
        фаворит проиграл: -2
        аутсайдер проиграл: -1
    Arguments:
        score: [8, 5]
        line: [1.54, 2.25]
    Return:
        [1, -1]
    """
    try:
        if score[0] > score[1]:
            return [1, -1] if line[0] < line[1] else [2, -2]
        else:
            return [-2, 2] if line[0] < line[1] else [-1, 1]
    except Exception:
        log_db.exception('From stat line')


def profit(score, odds):
    """
    Подсчитывает чистую прибыли при ставке на событие
    Функция не используеться !!!
    """
    if score[0] > score[1]:
        return [int(round((odds[0] - 1) * 100, 2)), -100]
    else:
        return [-100, int(round((odds[0] - 1) * 100, 2))]


def count_totl(side, score):
    """
    Считает дельту по тоталу
    Arguments:
        side: 'home' || 'away'
        score: [112, 98]
    Return:
        [True, 14, 210, 112]
        [False, -14, 210, 98]
    """
    try:
        total = score[0] + score[1]
        if side == 'home':
            return [True if score[0] > score[1] else False, score[0] - score[1], total, score[0]]
        else:
            return [True if score[1] > score[0] else False, score[1] - score[0], total, score[1]]
    except Exception:
        log_db.exception('From count_totl')


def count_handy(score, handy):
    """
    Считает дельту по форе
    Return:
        (7.5, -7.5)
    """
    home, away = score[0] - score[1], score[1] - score[0]
    if handy[0] < handy[1]:
        return home + handy[0], away + handy[1]
    else:
        return home + handy[0], away + handy[1]


def count_itot(handy, total):
    """
    Count individual total from
    total and handyCap value

    Arguments:
        handy: (48, (-7.5, 7.5), (1.87, 1.93), 0.06)
        total: (42, (200.5, 200.5), (1.88, 1.91), 0.03)
    Return:
        (98.5, 93,5)
    """
    hand = abs(handy[1][0])
    half = (total[1][0] - abs(handy[1][0])) / 2
    if half % 1 == 0:
        if handy[1][0] < 0:
            return half + hand, half + 0.5
        else:
            return half + 0.5, half + hand
    else:
        if handy[1][0] < 0:
            return half + hand - 0.5, half
        else:
            return half, half + hand - 0.5


def builder(mdata):
    """
        Buid match results

        Arguments: mdata =
            'teams': ['Venezia', 'Sassari']
            'link': '/basketball/italy/lega-a/venezia-sassari-tGwcHwNl/'
            'xeid': 'tGwcHwNl'
            'xhash': 'yjc0b'

            'meta':
                'season': '2014-2015'
                'league': 'lega-a'
                'country': 'italy'
                'sport': 'basketball'
                'seas_type': 'season'

            'score':
                'quat': ['19:21, 19:23, 22:10, 23:29, 7:17']
                'full': '90:100'
                'main': '83:83'
                'ot': True

            'date':
                'date': '11 Jun 2014'
                'time': '04:00'
                'datetime': '04-01-15 04:00'
                'timestamp': 1402448400

            'odds':
                'line': {
                    'ftot': {'mean': [1.83, 1.96], 'close': [1.85, 1.95],
                             'open': [1.82, 1.97]},
                    'frst': {'mean': [1.9, 1.92], 'close': [1.9, 1.93],
                             'open': [1.91, 1.92]}}
                'hand': {
                    'ftot': {'value': [-1.5, 1.5], 'mean': [2.59, 1.51],
                             'open': [2.56, 1.52], 'close': [2.62, 1.5]},
                    'frst': {'mean': [2.19, 1.71], 'value': [-0.5, 0.5],
                                  'open': [2.21, 1.7], 'close': [2.17, 1.72]}}
                'totl': {
                    'ftot': {'mean': [1.79, 2.02], 'value': [10.5, 10.5],
                             'open': [1.84, 1.97], 'close': [1.75, 2.08]},
                    'frst': {'mean': [1.89, 1.92], 'value': [6.0, 6.0],
                             'open': [1.93, 1.87], 'close': [1.84, 1.97]}}}

        Return:
          + 'sport': 'basketball'
          + 'country': 'usa'
          + 'league': 'NBA'
          + 'season': '2014/2015'
          + 'seas_type': 'play-offs'
          + 'link': 'http...san-antonio-spurs-miami-heat-67Upolsm/'
          + 'xeid': '67Upolsm'

          + 'datetime':
                'date': '11-06-14'
                'time': '04:00'
                'datetime': '11 Jun 2014 04:00'
                'timestamp': 1402448400
                'scraptime': '2014-11-25 13:50:44'

          + 'score':
                'full': '88:87'
                'ot': True
                'main': '78:78'
                'quat': ['19:15, 19:23, 19:14, 21:26, 10:9']

            'home':
                'team': 'Miami Heat'
              - 'tid': ????
                'ftot':
                    'result': [False, -17, 191, 87]
                    'delta': [-1, -5.5, -9.5, -7.5]
                    'profit': [23, 95, -100, 85]
                'frst':
                    'result': [False, -17, 191, 87]
                    'delta': [-1, -5.5, -9.5, -7.5]
                    'profit': [23, 95, -100, 85]
            'away':
                ....

            'odds':
                'ftot':
                    line: 'mean': [1.83, 1.96], 'close': [1.85, 1.95],
                          'open': [1.82, 1.97]
                    hand: 'value': [-1.5, 1.5], 'mean': [2.59, 1.51],
                          'open': [2.56, 1.52], 'close': [2.62, 1.5]
                    tots: 'mean': [1.79, 2.02], 'value': [10.5, 10.5],
                          'open': [1.84, 1.97], 'close': [1.75, 2.08]
                'frst':
                    line: 'mean': [1.9, 1.92], 'close': [1.9, 1.93],
                          'open': [1.91, 1.92]
                    hand: 'mean': [2.19, 1.71], 'value': [-0.5, 0.5],
                          'open': [2.21, 1.7], 'close': [2.17, 1.72]
                    totl: 'mean': [1.89, 1.92], 'value': [6.0, 6.0],
                          'open': [1.93, 1.87], 'close': [1.84, 1.97]
    """
    try:
        mdata['count_itot'] = count_itot(mdata['hcap'], mdata['totl'])
        dt = {
            'date': mdata['date'],
            'time': mdata['time'],
            'datetime': mdata['datetime'],
            'timestamp': mdata['timestamp'],
            'scraptime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        score = {
            'score': mdata['score'],
            'ot': mdata['ot'],
            'res_box': mdata['res_box']}

        st = stat_line(mdata['score'], mdata['line'])
        hc = count_handy(mdata['score'], mdata['hcap'][1])
        tl = (mdata['score'][0] + mdata['score'][1]) - mdata['totl'][1][0]
        it = (mdata['score'][0] - mdata['count_itot'][0],
              mdata['score'][1] - mdata['count_itot'][1])

        home = {
            'result': count_totl('home', mdata['score']),
            'delta': (st[0], hc[0], tl, it[0]),
            'profit': (
                int(mdata['line'][0] * 100 - 100) if st[0] > 0 else 0,
                int(mdata['hcap'][2][0] * 100 - 100) if hc[0] > 0 else 0,
                int(mdata['totl'][2][0] * 100 - 100) if tl > 0 else 0,
                91 if it[0] > 0 else 0)}

        # home['full'], home['short'] = get_teams(mdata['teams'][0])

        away = {
            'result': count_totl('away', mdata['score']),
            'delta': (st[1], hc[1], tl, it[1]),
            'profit': (
                int(mdata['line'][1] * 100 - 100) if st[1] > 0 else 0,
                int(mdata['hcap'][2][1] * 100 - 100) if hc[1] > 0 else 0,
                int(mdata['totl'][2][0] * 100 - 100) if tl > 0 else 0,
                91 if it[1] > 0 else 0)}

        # away['full'], away['short'] = get_teams(mdata['teams'][1])

        #  count nba link & betexplorer
        links = {
            'oddsportal': 'http://www.oddsportal.com/' + mdata['link'],
            'nba': '',
            'betxplorer': ''}

        odds = {
            'line': mdata['line'],
            'handy': (
                (mdata['hcap'][1][0], mdata['hcap'][2][0]),
                (mdata['hcap'][1][1], mdata['hcap'][2][1])),
            'total': (
                mdata['totl'][1][0], mdata['totl'][2][1], mdata['totl'][2][1]),
            'indy': (
                (mdata['count_itot'][0], 1.91, 1.91),
                (mdata['count_itot'][1], 1.91, 1.91))}

        new_match = dict(
            sport='basketball',
            league='NBA',
            season=mdata['season'],
            type=mdata['type'],
            xeid=mdata['xeid'],
            datetime=dt,
            home=home,
            away=away,
            odds=odds,
            score=score,
            links=links)

        return new_match

    except Exception:
        log_db.exception('Builder function err')

if __name__ == '__main__':
    match_data = {
        'season': '2014/2015',
        'ot': False,
        'hash': 'yj1b4',
        'xeid': '67Upolsm',
        'type': 'play-offs',
        'score': [104, 87],
        'link': '/basketball/usa/nba-2013-2014/san-antonio-spurs-miami-heat-67Upolsm/',
        'teams': ['San Antonio Spurs', 'Miami Heat'],
        'res_box': '22:29, 25:11, 30:18, 27:29',
        'date': '11-06-14',
        'timestamp': 1402448400,
        'time': '04:00',
        'datetime': '11 Jun 2014 04:00',
        'line': (1.28, 3.65),
        'hcap': (48, (-11.5, 11.5), (1.92, 1.89), 0.03),
        'totl': (38, (200.5, 200.5), (1.9, 1.91), 0.01)}

    # print(builder(match_data))
    print(count_handy([112, 98], [-6.5, 6.5]))
