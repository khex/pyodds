#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from collections import UserDict
# from logger import log_db
odds_value = []


class Match(UserDict):
    """docstring for Match @ ???
    {
        "_id": {
            "$oid": "5659b66817fb2501342104d8"
        },
        "seas_list": ["2015-2016", ...,   "2005-2006"],
        "score": {
            "quat": ["36:29, 22:24, 24:32, 19:31"],
            "full": "101:116",
            "ot": false
        },
        "country": "usa",
        "seas_type": "season",
        "home": {
            "team": "Memphis Grizzlies",
            "tid": 15,
            "frst": {},
            "ftot": {
                "profit": [-100, -100, 89, 0],
                "delta": [-4.5, -18.5, 21.5, 0],
                "oddval": [1, -3.5, 195.5, 0],
                "resalt": [-3.5, -15, 217, 101]
            }
        },
        "date": {
            "ts": "1448672400",
            "datetime": "15-11-28 03:00",
            "date": "28-11-2015",
            "time": "03:00",
            "scraptime": {"$date": "2015-11-28T14:12:56.404Z"},
            "iso": {"$date": "2015-11-28T03:00:00.000Z"},

        },
        "away.ftot.delta"
        "away": {
            "team": "Atlanta Hawks",
            "tid": 1,
            "frst": {},
            "ftot": {
                "profit": [125, 86, 89, 0],
                "delta": [4.5, 18.5, 21.5, 0],
                "oddval": [-1, 3.5, 195.5, 0],
                "resalt": [3.5, 15, 217, 116]
            }
        },
        "league": "nba",
        "odds": {
            "totl": {
                "ftot": {
                    "mean": [1.9, 1.92],
                    "open": [1.89, 1.93],
                    "value": [195.5, 195.5],
                    "close": [1.9, 1.92]
                }
            },
            "hand": {
                "ftot": {
                    "mean": [1.95, 1.86],
                    "open": [1.93, 1.88],
                    "value": [-3.5, 3.5],
                    "close": [1.97, 1.85]
                }
            },
            "line": {
                "ftot": {
                    "mean": [1.64, 2.26],
                    "open": [1.63, 2.27],
                    "close": [1.65, 2.25]
                }
            },
            "itot": {
                "mean": [1.89, 1.89],
                "open": [1.89, 1.89],
                "value": [99.5, 96.5],
                "close": [1.89, 1.89],
            }
        },
        "xeid": "46Qm9Gjh",
        "link": "/basketball/usa/nba/memphis-grizzlies-atlanta-hawks-46Qm9Gjh/",
        "sport": "basketball"
    }
    """

    def __init__(self, dd):
        """ dd as dict_data
        {
            'meta': {
                'seas_list': ['2015-2016', '2014-2015', ..., '2006-2007', '2005-2006'],
                'seas_type': 'season',
                'league': 'nba',
                'sport': 'basketball',
                'country': 'usa'
            },
            'xeid': 'rVOKhzkE',
            'tids': [22, 20],
            'teams': ['Orlando Magic', 'New York Knicks'],
            'link': '/basketball/usa/nba/orlando-magic-new-york-knicks-rVOKhzkE/',
            'xhash': 'yj957',
            'score': {'full': '100:91', 'ot': False, 'quat': ['20:17, 26:18, 26:28, 28:28']},
            'odds': {
                'hand': {'ftot': {'open': [1.90, 1.91], 'value': [-1.5, 1.5], 'mean': [1.91, 1.91], 'close': [1.92, 1.91]}},
                'line': {'ftot': {'open': [1.79, 2.01], 'close': [1.8, 2.0], 'mean': [1.79, 2.0]}},
                'itot': {'ftot': {'mean': [1.89, 1.89], 'value': [115.5, 98.5], 'close': [1.89, 1.89], 'open': [1.89, 1.89]}},
                'totl': {'ftot': {'open': [1.90, 1.91], 'value': [195.5, 195.5], 'mean': [1.92, 1.9], 'close': [1.94, 1.88]}}
            },
            'date': {'ts': '1448496000', 'iso': datetime.datetime(2015, 11, 26, 2, 0),
                     'date': '26-11-2015', 'time': '02:00', 'datetime': '15-11-26 02:00'
            }
        }
        """

        self.data = {'home': {'ftot': {}, 'frst': {}},
                     'away': {'ftot': {}, 'frst': {}}}

        self.update(dd['meta'])
        self['link'] = dd['link']
        self['xeid'] = dd['xeid']
        self['date'] = dd['date']
        self['score'] = dd['score']
        self['odds'] = dd['odds']  # может в каждую команду отдельно???

        # self['date']['scraptime'] = datetime.now().strftime('%y-%m-%d %H:%M')
        self['date']['scraptime'] = datetime.datetime.utcnow()
        self['home']['team'], self['away']['team'] = dd['teams']
        self['home']['tid'], self['away']['tid'] = dd['tids']

        # counting Full Time & Over Time
        once_scrd = self.count_result(dd['score']['full'], dd['odds']['line']['ftot'])
        (self['home']['ftot']['resalt'], self['away']['ftot']['resalt']) = once_scrd

        scor = [int(s) for s in dd['score']['full'].split(':')]
        line = self.count_line(scor, dd['odds']['line']['ftot'], once_scrd)
        hand = self.count_handy(scor, dd['odds']['hand']['ftot'])
        totl = self.count_total(scor, dd['odds']['totl']['ftot'])
        # itot = [[0, 0], [0, 0], [0, 0]]
        itot = self.count_i_tot(scor, dd['odds']['itot']['ftot'])

        self['home']['ftot']['delta'], self['away']['ftot']['delta'] = [
            [line[0][n], hand[0][n], totl[0][n], itot[0][n]] for n in range(0, 2)]

        self['home']['ftot']['profit'], self['away']['ftot']['profit'] = [
            [line[1][n], hand[1][n], totl[1][n], itot[1][n]] for n in range(0, 2)]

        self['home']['ftot']['oddval'], self['away']['ftot']['oddval'] = [
            [line[2][n], hand[2][n], totl[2][n], itot[2][n]] for n in range(0, 2)]

        """ counting First Half if Odds exist
        if dd['odds']['line']['frst']:
            line = self.count_line()
            hand = self.count_handy()
            totl = self.count_total()
            itot = self.count_i_tot()

            once_scrd = self.count_result(dd['score']['full'])
            (self['home']['frst']['resalt'],
             self['away']['frst']['resalt']) = once_scrd

            self['home']['frst']['delta'], self['away']['frst']['delta'] = [
                [line[0][n], hand[0][n], totl[0][n], itot[0][n]] for n in range(0, 2)]

            self['home']['frst']['profit'], self['away']['frst']['profit'] = [
                [line[1][n], hand[1][n], totl[1][n], itot[1][n]] for n in range(0, 2)]
        """

    def count_result(self, schet, odds):

        """ Возвращает результат в очках для каждой команды

            Arguments:
                score @ str: '90:100'

            Return: [ [1.5, 14, 210, 112], [-1.5, -14, 210, 98]]
        """
        global odds_value
        score = [float(s) for s in schet.split(':')]  # [90, 100]
        home_win = True if score[0] > score[1] else False

        # равные ли команды по кф. ~ 0.9
        if abs(odds['mean'][0] - odds['mean'][1]) < 0.1:
            reslt = [2.5, -2.5] if home_win else [-2.5, 2.5]
            odds_value = [0, 0]
        else:
            if odds['mean'][0] < odds['mean'][1]:
                reslt = [1.5, -1.5] if home_win else [-3.5, 3.5]
                odds_value = [1.0, -1.0]
            else:
                reslt = [3.5, -3.5] if home_win else [-1.5, 1.5]
                odds_value = [-1.0, 1.0]

        handy = [float(score[0] - score[1]), float(score[1] - score[0])]
        total = float(sum(score))

        return [[reslt[n], handy[n], total, score[n]] for n in range(0, 2)]
        """
        return [[reslt[0], handy[0], total, score[0]],
                [reslt[1], handy[1], total, score[1]]]
        except Exception:
            log_db.exception('From count_totl')
        """

    def count_line(self, score, odds, once_scrd):
        global odds_value
        """ Подсчет дельты и прибыли матча & профит:

            Arguments:
                score: [90, 100]
                odds: [1.54, 2.25]
                once_scrd: [[1.5, 14, 210, 112], [-1.5, -14, 210, 98]]

            Return:
                [[1, 54], [-1, -100]]
        """
        delta, profit = [], []

        # подсчет дельты
        once = [m[0] for m in once_scrd]
        if once == [1.5, -1.5]:
            delta = [0.5, -0.5]
        elif once == [2.5, -2.5]:
            delta = [1.5, -1.5]
        elif once == [3.5, -3.5]:
            delta = [4.5, -4.5]
        elif once == [-1.5, 1.5]:
            delta = [-0.5, 0.5]
        elif once == [-2.5, 2.5]:
            delta = [-2.5, 2.5]
        elif once == [-3.5, 3.5]:
            delta = [-4.5, 4.5]
        else:
            raise BaseException('Hernja s deltoj')

        # подсчет прибыли
        if score[0] > score[1]:
            profit = [int((odds['mean'][0] - 1) * 100), -100]
        else:
            profit = [-100, int((odds['mean'][1] - 1) * 100)]

        # odds_val из глобальной переменной
        return [delta, profit, odds_value]

    def count_handy(self, score, handy):
        print(score, handy)
        """
        Считает дельту по форе & профит:
        Return:
            (7.5, -7.5)
        """
        delta = [
            self['home']['ftot']['resalt'][1] + handy['value'][0],
            self['away']['ftot']['resalt'][1] + handy['value'][1]
        ]

        # подсчет прибыли
        if delta[0] > delta[1]:
            profit = [int((handy['mean'][0] - 1) * 100), -100]
        else:
            profit = [-100, int((handy['mean'][1] - 1) * 100)]

        return [delta, profit, handy['value']]

    def count_total(self, score, total):
        """ Считатет дельту тотала & профит """
        if total['value'] == [0, 0]:
            return [[0, 0], [0, 0]]

        delta = self['home']['ftot']['resalt'][2] - total['value'][0]

        # подсчет прибыли
        if delta > 0:
            profit = int((total['mean'][0] - 1) * 100)
        else:
            profit = -100

        return [[delta, delta], [profit, profit], total['value']]

    def count_i_tot(self, score, itot):
        """ Считатет инд. тотал & профит """
        if itot['value'] == [0, 0]:
            return [[0, 0], [0, 0]]

        delta = [self['home']['ftot']['resalt'][3] - itot['value'][0],
                 self['away']['ftot']['resalt'][3] - itot['value'][1]]

        profit = [int((itot['mean'][0] - 1) * 100) if delta[0] > 0 else -100,
                  int((itot['mean'][1] - 1) * 100) if delta[1] > 0 else -100]

        return [delta, profit, itot['value']]

if __name__ == '__main__':
    base = {
        'teams': ['Toronto Blue Jays', 'Boston Red Sox'],
        'link': '/baseball/usa/mlb/toronto-blue-jays-boston-red-sox-4G79dfXC/',
        'xhash': 'yj17d',
        'xeid': '4G79dfXC',
        'meta': {
            'season': '2015',
            'seas_type': 'season',
            'sport': 'baseball',
            'country': 'usa',
            'league': 'mlb'},
        'date': {
            'timestamp': 1435770420,
            'date': '01 Jul 2015',
            'datetime': '01-07-15 20:07',
            'time': '20:07'},
        'score': {
            'full': '11:2',
            'ot': False,
            'quat': '5:0, 2:0, 1:0, 0:0, 0:0, 1:0, 0:1, 2:1, X:0',
            'main': ''},
        'odds': {
            'itot': {
                'ftot': {
                    'mean': [1.89, 1.89],
                    'value': [4.5, 3.5]}},
            'totl': {
                'ftot': {
                    'value': [8.5, 8.5], 'mean': [1.86, 1.94],
                    'open': [1.83, 1.98], 'close': [1.9, 1.9]},
                'frst': {
                    'value': [4.5, 4.5], 'mean': [1.88, 1.92],
                    'open': [1.87, 1.93], 'close': [1.88, 1.92]}
            },
            'line': {
                'ftot': {
                    'open': [1.67, 2.2],
                    'close': [1.68, 2.18],
                    'mean': [1.67, 2.19]},
                'frst': {
                    'open': [1.66, 2.27],
                    'close': [1.68, 2.23],
                    'mean': [1.67, 2.25]}
            },
            'hand': {
                'ftot': {
                    'value': [-1.5, 1.5], 'mean': [2.37, 1.6],
                    'open': [2.34, 1.61], 'close': [2.39, 1.59]},
                'frst': {
                    'value': [-0.5, 0.5], 'mean': [1.92, 1.85],
                    'open': [1.92, 1.89], 'close': [1.92, 1.82]}
            }
        }
    }
    m = Match(base)
    print(m)
