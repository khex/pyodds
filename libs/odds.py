#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/khex/Code/pyodds/libs')

import ujson
import requests
# import multiprocessing as mp
from statistics import mean
from logger import log_odds
""" @doc-bug: MLB если pre-season и нет данніх линии - еррор """
""" Для каждого вида спорта отдельно
    home_away  -> get_page -> map_close -> get_odds  > asian_handy -> get_page -> map_close  >
    /  home_away -> get_page -> map_close /
"""

def get_page(pref, xeid, xhash, value):
    """
        Строит ссылку из параметров, при помощи requests
        запрашивает JSON с данными коэф. на метч и парсит их
        в питоновский словарь. Ex.: 'feed_home_away.js'

        Arguments:
            pref: адреса '1-6' -> бейсбол
            xeid: 'UX19OwXR'
            xhash: 'yja8d'
            value: '3-3' -> frst

        Return: {
            'oddsdata': ...,
            'history': ...}
    """
    try:
        # 'http://fb.oddsportal.com/feed/match/1-3-UX19OwXR-3-1-yja8d.dat'
        domain = 'http://fb.oddsportal.com/feed/match'
        link_text = '{}/{}-{}-{}-{}.dat'
        link = link_text.format(domain, pref, xeid, value, xhash)
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'referer': 'https://www.oddsportal.com/basketball/usa/nba/philadelphia-76ers-dallas-mavericks-fL8bbADr/'
        }
        r = requests.get(link, headers=headers)  # r.encoding = 'ISO-8859-1'
        if r.status_code != 200:
            raise('results page status code is {}'.format(r.status_code))

        """  в отдельную функцию ету из tabler.py json_cuter.py   """
        r_string = str(r.content)[68:-3]
        params = ujson.loads(r_string)
        """ partals/feed_home_away.js
        ['d']['oddsdata']['back']- массив кф. на мамент начала собития
        ['d']['history']['back'] - массив кф. с начала прийома ставок
        """

        return {'close': params['d']['oddsdata']['back'],
                'history': params['d']['history']['back']}

    except Exception:
        log_odds.exception('get_page ERROR')


def map_close(odds_arry):
    """
        Мапит массив коэф.. на момент закрытия

        Arguments:
            Dict of lists or dicts
            {"392":[1.72,2.15], "78":[2.13,1.81], "49":[2.07,1.76]}  or
            ['424': {'0': 2.59, '1': 1.51}, ... , '406': {'0': 2.6, '1': 1.53}]

        Return:
            [1.75, 1.91]
    """
    try:
        if type(list(odds_arry.values())[0]) is list:
            # odds -> list
            arry_home = [odds[0] for odds in odds_arry.values()]
            arry_away = [odds[1] for odds in odds_arry.values()]

        else:
            # odds -> dict
            arry_home = [odds['0'] for odds in odds_arry.values()]
            arry_away = [odds['1'] for odds in odds_arry.values()]

        return [round(mean(arry_home), 2),
                round(mean(arry_away), 2)]

    except Exception:
        log_odds.exception('Can\'t map_close')


def map_open(odds_arry, tids):
    """
        Выбирает самые ранние, по времени, коэф..
        на момент открытия и мапит их

        Arguments:
            tids = ["221hix2rrhkx0x48k1v", "221hix2rrhkx0x48k20"]
            "back":{
                "221hix2rrhkx0x48k1v":{
                    "2":[ ["1.91", null, 1433076947], ... , ["2.09", null, 1433116298]],
                    "392":[[1.72,0,1432939158]], ...
                    "78":[["2.07",null,1433116478], ...
                "221hix2rrhkx0x48k20":{
                    "2":[["1.91",null,1433076947], ...
                    "392":[[2.15,0,1432939158]], ...
                    "78":[["1.85",null,1433116478], ...

        Return:
            [1.89, 1.91]
    """

    home_arry = [float(odd[-1][0]) for odd in odds_arry[tids[0]].values()]
    away_arry = [float(odd[-1][0]) for odd in odds_arry[tids[1]].values()]

    return [round(mean(home_arry), 2),
            round(mean(away_arry), 2)]


def one_x_two():
    """
    Коэф. на 1X2
    """
    pass


def home_away(pref, xeid, xhash, args_dict):
    """
        Коэф. на Home/Away

        Arguments:
            pref: '1-6' -> бейсбол
            xeid:  '67Upolsm'
            xhash: 'yj1b4'
            args_dict: dict(ftot='3-1', frst='3-3')

        Return: {
            'ftot': {
                'mean': [1.83, 1.96],
                'close': [1.85, 1.95],
                'open': [1.82, 1.97]},
            'frst': {
                'mean': [1.9, 1.92],
                'close': [1.9, 1.93],
                'open': [1.91, 1.92]}}
    """
    try:
        resp_dict = {}
        for period, value in args_dict.items():
            # period: 'ftot', value: '3-1',
            # period: '1st Half', value: '3-3'
            resp_dict[period] = {}

            # get JSON resalts
            odds_dict = get_page(pref, xeid, xhash, value)
            mtch_type = 'E-{}-0-0-0'.format(value)

            # season = "OutcomeID":["221hix2rrhkx0x48k1v","221hix2rrhkx0x48k20"]
            # 'pre-season' = {'close': None, 'history': None}
            if odds_dict['close']:
                tids = odds_dict['close'][mtch_type]['OutcomeID']
                tids = tids if type(tids) is list else [tids['0'], tids['1']]

                # ???
                close_odds = map_close(odds_dict['close'][mtch_type]['odds'])
                open_odds = map_open(odds_dict['history'], tids)

                resp_dict[period]['close'] = close_odds
                resp_dict[period]['open'] = open_odds
                resp_dict[period]['mean'] = [
                    round(mean([close_odds[0], open_odds[0]]), 2),
                    round(mean([close_odds[1], open_odds[1]]), 2)]

            else:
                resp_dict[period]['close'] = [0, 0]
                resp_dict[period]['open'] = [0, 0]
                resp_dict[period]['mean'] = [0, 0]

        return resp_dict

    except Exception:
        log_odds('From home_away_func()')


def asian_handy(pref, xeid, xhash, args_dict):
    """
        Коэф. на Asian Handicap

        Arguments:
            pref: '1-6' -> бейсбол
            xeid:  '67Upolsm'
            xhash: 'yj1b4'
            args_dict: dict(ftot='5-1', frst='5-3')

        Returns: {
            'ftot': {
                'open': [2.56, 1.52],
                'close': [2.62, 1.5],
                'mean': [2.59, 1.51],
                'value': [-1.5, 1.5]},
            'frst': {
                'open': [2.21, 1.7],
                'close': [2.17, 1.72],
                'mean': [2.19, 1.71],
                'value': [-0.5, 0.5]}}
    """
    pref, xeid, xhash, args_dict
    try:
        resp_dict = {}
        for period, value in args_dict.items():  # period: 'ftot', value: '3-1'

            mtch_type, max_odds, handy_value, tids = '', 0, 0, []
            resp_dict[period] = {}

            odds_dict = get_page(pref, xeid, xhash, value)

            if odds_dict['close']:
                for key, value in odds_dict['close'].items():
                    temp_odds = len(value['odds'].items())
                    if temp_odds > max_odds:
                        max_odds = temp_odds
                        mtch_type = key
                        tids = value['OutcomeID']
                        handy_value = float(value['handicapValue'])

                resp_dict[period]['value'] = [handy_value, -1 * handy_value]
                close_odds = map_close(odds_dict['close'][mtch_type]['odds'])

                tids = tids if type(tids) is list else [tids['0'], tids['1']]
                open_odds = map_open(odds_dict['history'], tids)

                resp_dict[period]['close'] = close_odds
                resp_dict[period]['open'] = open_odds
                resp_dict[period]['mean'] = [
                    round(mean([close_odds[0], open_odds[0]]), 2),
                    round(mean([close_odds[1], open_odds[1]]), 2)]

            else:
                resp_dict[period]['value'] = [0, 0]
                resp_dict[period]['close'] = [0, 0]
                resp_dict[period]['open'] = [0, 0]
                resp_dict[period]['mean'] = [0, 0]

        return resp_dict

    except Exception:
        log_odds.exception('From asian_handy()')


def over_under(pref, xeid, xhash, args_dict):
    """
        Коэф. на Over/Under

        Arguments:
            pref: '1-6' -> бейсбол
            xeid:  '67Upolsm'
            xhash: 'yj1b4'
            args_dict: dict(ftot='5-1', frst='5-3')

        Returns: {
            'ftot': {
                'open': [1.84, 1.97],
                'close': [1.75, 2.08],
                'mean': [1.79, 2.02],
                'value': [10.5, 10.5]},
            'frst': {
                'open': [1.93, 1.87],
                'close': [1.84, 1.97],
                'mean': [1.89, 1.92],
                'value': [6.0, 6.0]}}
    """
    try:
        resp_dict = {}
        for period, value in args_dict.items():  # period: 'ftot', value: '3-1'

            mtch_type, max_odds, handy_value, tids = '', 0, 0, []
            resp_dict[period] = {}

            odds_dict = get_page(pref, xeid, xhash, value)

            if odds_dict['close']:
                for key, value in odds_dict['close'].items():

                    temp_odds = len(value['odds'].items())
                    temp_valu = float(value['handicapValue'])

                    if temp_odds > max_odds and temp_valu % 1 != 0:
                        max_odds = temp_odds
                        mtch_type = key
                        tids = value['OutcomeID']
                        handy_value = temp_valu

                resp_dict[period]['value'] = [handy_value, handy_value]
                close_odds = map_close(odds_dict['close'][mtch_type]['odds'])

                tids = tids if type(tids) is list else [tids['0'], tids['1']]
                open_odds = map_open(odds_dict['history'], tids)

                resp_dict[period]['close'] = close_odds
                resp_dict[period]['open'] = open_odds
                resp_dict[period]['mean'] = [
                    round(mean([close_odds[0], open_odds[0]]), 2),
                    round(mean([close_odds[1], open_odds[1]]), 2)]
                """
                print('value: {} mean: {} delta: {}, amount: {}'.format(
                    resp_dict[period]['value'][0],
                    resp_dict[period]['mean'],
                    abs(round(resp_dict[period]['mean'][0] - resp_dict[period]['mean'][1], 2)),
                    max_odds
                ))
                """
            else:
                resp_dict[period]['value'] = [0, 0]
                resp_dict[period]['close'] = [0, 0]
                resp_dict[period]['open'] = [0, 0]
                resp_dict[period]['mean'] = [0, 0]

        return resp_dict

    except Exception:
        log_odds.exception('From asian_handy()')


def odds_even():
    """
    Коэф. на Odd or Even
    """
    pass


def itot_base(line, total):
    """
    импровизированные данные, нужно пересчитать
    """
    if total == 5.5:
        return 2.5
    elif total == 6.5:
        return 3.5 if line < 2 else 2.5
    elif total == 7.5:
        return 4.5 if line < 1.7 else 3.5 if line < 2.7 else 2.5
    elif total == 8.5:
        return 4.5 if line < 1.9 else 3.5
    elif total == 9.5:
        return 5.5 if line < 1.55 else 4.5 if line < 2.2 else 3.5
    elif total == 10.5:
        return 5.5 if line < 2 else 4.5
    elif total == 11.5:
        return 6.5 if line < 1.4 else 5.5 if line < 1.75 else 4.5
    elif total == 12.5:
        # переделать, взято из предыдущего
        return 7.5 if line < 1.4 else 6.5 if line < 1.75 else 5.5
    else:
        raise BaseException('Baseball total: {}'.format(total))


def itot_basket(total, h_cap):
    """
    Returns:
        a value of individual handyCap like:
        92.5 or 101.5
    """
    abs_cup = abs(h_cap)
    half_totl = (total - abs_cup) / 2  # 95.0 or 95.5
    hand_even = (abs_cup - 0.5) % 2 == 0
    # тотал > чет
    if (total - 0.5) % 2 == 0:
        # фора > чет
        if hand_even:
            return half_totl + abs_cup if h_cap < 0 else half_totl + 0.5
        # фора > нечет
        else:
            return half_totl + abs_cup + 0.5 if h_cap < 0 else half_totl
    # тотал > нечет
    else:
        # фора > чет
        if hand_even:
            return half_totl + abs_cup + 0.5 if h_cap < 0 else half_totl
        # фора > нечет
        else:
            return half_totl + abs_cup if h_cap < 0 else half_totl + 0.5


def itot_hockey(total, h_cap):
    return 17.5


def get_odds(sport, xeid, xhash):
    """         1x2   O/U   H/A   Asian   O/E
    FTOT        1-1   2-1   3-1    5-1   10-1
    Full Time   1-2   2-2   3-2    5-2   10-2
    1st Half    1-3   2-3   3-3    5-3   10-3
    2nd Half    1-4   2-4   3-4    5-4   10-4
    1 Quater    1-8   2-8   3-8    5-8   10-8
    2 Quater    1-9   2-9   3-9    5-9   10-9
    3 Quater    1-10  2-10  3-10   5-10  10-10
    4 Quater    1-11  2-11  3-11   5-11  10-11
    """
    resp = {}
    if sport == 'baseball':
        resp['line'] = home_away('1-6', xeid, xhash, {'ftot': '3-1'})  # , frst='3-3')))
        resp['hand'] = asian_handy('1-6', xeid, xhash, {'ftot': '5-1'})  # , frst='5-3'))),
        resp['totl'] = over_under('1-6', xeid, xhash, {'ftot': '2-1'})   #

        resp_totl = resp['totl']['ftot']['value']
        resp_hand = resp['hand']['ftot']['value']

        # params: line, total
        itot_home = itot_base(resp['line']['ftot']['mean'][0], resp_totl[0])
        itot_away = itot_base(resp['line']['ftot']['mean'][1], resp_totl[1])

        resp['itot'] = {'ftot': dict(
            value=[itot_home, itot_away],
            mean=[1.89, 1.89],
            open=[1.89, 1.89],
            close=[1.89, 1.89]
        )}

        """      
        pool.close()
         { для 'pre-seas' нет Тотал значения
        'hand': {
            'frst': {},
            'ftot': {'mean': [2.25, 1.65], 'value': [-1.5, 1.5], 'close': [2.25, 1.65], 'open': [2.25, 1.65]}},
        'line': {
            'frst': {},
            'ftot': {'open': [1.71, 2.11], 'close': [1.7, 2.12], 'mean': [1.71, 2.12]}},
        'totl': {
            'ftot': {},
            'frst': {}}
        }
        считать только когда присутств Линия и Тотал (имеют значение не [0, 0])
        if resp['line']['ftot']['mean'] != [0, 0] and resp['totl']['ftot']['value'] != [0, 0]:
            resp['itot'] = dict(ftot={
                'mean': [1.89, 1.89], 'open': [0, 0], 'close': [0, 0],
                'value': [itot_base(resp['line']['ftot']['mean'][0], resp['totl']['ftot']['value'][0]),
                          itot_base(resp['line']['ftot']['mean'][1], resp['totl']['ftot']['value'][1])]})
        else:
            resp['itot'] = dict(ftot={'value': [0, 0], 'mean': [0, 0], 'open': [0, 0], 'close': [0, 0]})

        """
        return resp

    if sport == 'basketball':

        resp['line'] = home_away('1-3', xeid, xhash, {'ftot': '3-1'})  # , frst='3-3')))
        resp['hand'] = asian_handy('1-3', xeid, xhash, {'ftot': '5-1'})  # , frst='5-3'))),
        resp['totl'] = over_under('1-3', xeid, xhash, {'ftot': '2-1'})   # , frst='2-3')))}

        resp_totl = resp['totl']['ftot']['value']
        resp_hand = resp['hand']['ftot']['value']

        itot_home = itot_basket(resp_totl[0], resp_hand[0])
        itot_away = itot_basket(resp_totl[1], resp_hand[1])

        resp['itot'] = {'ftot': dict(
            value=[itot_home, itot_away],
            mean=[1.89, 1.89],
            open=[1.89, 1.89],
            close=[1.89, 1.89]
        )}

        """
        Написчать iTotal функцию для баскетбола
        # считать только когда присутствует Линия и Тотал (имеют значение не [0, 0])
        if resp['line']['ftot']['mean'] != [0, 0] and resp['totl']['ftot']['value'] != [0, 0]:
            resp['itot'] = dict(ftot={
                'mean': [1.89, 1.89], 'open': [0, 0], 'close': [0, 0],
                'value': [itot_base(resp['line']['ftot']['mean'][0],
                                    resp['totl']['ftot']['value'][0]),
                          itot_base(resp['line']['ftot']['mean'][1],
                                    resp['totl']['ftot']['value'][1])]})
        else:
            resp['itot'] = dict(ftot={'value': [0, 0], 'mean': [0, 0], 'open': [0, 0], 'close': [0, 0]})
        """

        return resp

    if sport == 'hockey':

        resp['line'] = home_away('1-4', xeid, xhash, {'ftot': '3-1'})    # , frst='3-3')))
        resp['hand'] = asian_handy('1-4', xeid, xhash, {'ftot': '5-1'})  # , frst='5-3'))),
        resp['totl'] = over_under('1-4', xeid, xhash, {'ftot': '2-1'})   # , frst='2-3')))}

        resp_totl = resp['totl']['ftot']['value']
        resp_hand = resp['hand']['ftot']['value']

        itot_home = itot_hockey(resp_totl[0], resp_hand[0])
        itot_away = itot_hockey(resp_totl[1], resp_hand[1])

        resp['itot'] = {
            'ftot': dict(value=[itot_home, itot_away], mean=[1.89, 1.89], open=[1.89, 1.89], close=[1.89, 1.89])
        }

        return resp

if __name__ == '__main__':
    """ {
        'hand': {
            'ftot': {
                'close': [1.9, 1.88],
                'mean': [1.9, 1.88],
                'open': [1.89, 1.89],
                'value': [-3.5, 3.5]},
            'frst': {
                'close': [1.87, 1.88],
                'mean': [1.87, 1.89],
                'open': [1.86, 1.9],
                'value': [-1.5, 1.5]}},
        'line': {
            'ftot': {
                'close': [1.58, 2.29],
                'mean': [1.56, 2.33],
                'open': [1.55, 2.36]},
            'frst': {
                'close': [1.64, 2.14],
                'mean': [1.62, 2.17],
                'open': [1.61, 2.19]}},
        'totl': {
            'ftot': {
                'close': [1.84, 1.92],
                'mean': [1.85, 1.92],
                'open': [1.85, 1.91],
                'value': [165.5, 165.5]},
            'frst': {
                'close': [1.87, 1.87],
                'mean': [1.88, 1.86],
                'open': [1.88, 1.85],
                'value': [82.5, 82.5]}}
        }
    """
    # basketball/usa/nba/portland-trail-blazers-memphis-grizzlies-lpZAkkL7/
    # sport, xeid, xhash = 'basketball', 'lpZAkkL7', 'yj749'
    sport, xeid, xhash = 'baseball', 'OMcw0nF8','yjdbb'
    respont = get_odds(sport, xeid, xhash)

    print(respont)
