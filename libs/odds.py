#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import multiprocessing as mp
from logger import log_odds

""" JSON
json.JSONDecoder():
json.dumps(): dict() > json

json.JSONDecoder()
json.loads(): decoding > string > dict()
"""

"""      \  home_away  -> get_page -> map_odds \
get_odds  > h_cap -> get_page -> map_odds  >
         /  total -> get_page -> map_odds /
"""


def get_page(prefix, form, xhash):
    """
    Helper func to home_away() & hcap_totl()
    that recieve JSON from remote oddsportal
    1-3-UX19OwXR-2-1-yja8d.dat?_=1415473649648
    1-3-UX19OwXR-3-1-yja8d.dat?_=1415473649648
    1-3-UX19OwXR-5-1-yja8d.dat?_=1415473715925

    Params:
        prefix: адреса '1-3-UX19OwXR' -> вид спорта + xeid
        form: of betting like 'home_away', 'h_cap', 'total'
        xhash: 'yja8d'

    Return {
        'oddsdata': ...,
        'history': ...
        }
    """
    try:
        # 'http://fb.oddsportal.com/feed/match/1-3-UX19OwXR-3-1-yja8d.dat'
        domain = 'http://fb.oddsportal.com/feed/match/'
        form_dict = {'home_away': '-3-1-', 'h_cap': '-5-1-', 'total': '-2-1-'}

        link_text = '{}feed/match/{}{}{}.dat'
        link = link_text.format(domain, prefix, form_dict[form], xhash)

        r = requests.get(link).encoding = 'ISO-8859-1'

        """  !!!! а может в отдельную функцию ету из tabler.py ???
        обложить тестами
        """
        r_string = str(r.content)
        starts = r_string.find(".dat\\',") + 8
        params = json.loads(r_string[starts:-3])

        """
        ['d']['oddsdata']['back']- массив кф. на мамент начала собития
        ['d']['history']['back'] - массив истории кф. с начала открытия
        """
        return {
            'oddsdata': params['d']['oddsdata']['back'],
            'history': params['d']['history']['back']
        }
    except Exception:
        log_odds.exception('get_page ERROR')


def map_odds(odds_arry):
    """
    Вспомогательная функция, которая из JSON словаря
    высчитывает средее геометрическое.

    Arguments:
        odds_arry: { 'E-3-1--3.5-0-0': ... , }

    Return {
        'home': (mean, avrg_open, avrg_close),
        'away': (mean, avrg_open, avrg_close),
        mean = (avrg_open + avrg_close) / 2
    }
    """
    try:
        arr_len = len(odds_arry)
        if type(odds_arry[0]) is list:
            home = sum([val[0] for val in odds_arry]) / arr_len
            away = sum([val[1] for val in odds_arry]) / arr_len
        else:
            home = sum([val['0'] for val in odds_arry]) / arr_len
            away = sum([val['1'] for val in odds_arry]) / arr_len
        return {
            'length': arr_len,
            'home': round(home, 2),
            'away': round(away, 2),
            'delta': round(abs(home - away), 2),
        }
    except Exception:
        log_odds.exception('Can not map_odds')


def one_x_two():
    pass


def home_away(xeid, xhash):
    """
    Get values of home_away odds

    :param
        xeid:  '67Upolsm'
        xhash: 'yj1b4'
    :return
        (1.27, 2.55)
    """
    try:
        odds_dict = get_page(xeid, xhash, 'home_away')['E-3-1-0-0-0']['odds']
        if odds_dict is not None:
            odds_arry = [odds_dict[item] for item in odds_dict]
            data = map_odds(odds_arry)
            if data is not None:
                return data['home'], data['away']
    except Exception:
        log_odds('From home_away_func()')


def h_cap(xeid, xhash, odd_type):
    """
    Get values of total and handyCaps

    :param
        xeid:     '67Upolsm'
        xhash:    'yj1b4'
        odd_type: 'hcap' or 'total'
    :return
        (48, (-7.5, 7.5), (1.87, 1.93), 0.06) or
        (42, (200.5, 200.5), (1.88, 1.91), 0.03)
    """
    try:
        arry = []
        odds_dict = get_page(xeid, xhash, odd_type)
        if odds_dict is not None:
            for key, val in odds_dict.iteritems():
                hcap_value = float(val["handicapValue"])
                odds_dict = val['odds']
                odds_arry = [odds_dict[item] for item in odds_dict]
                if hcap_value % 1 != 0:
                    data = map_odds(odds_arry)

                    if data is not None:
                        arry.append((
                            data['length'],
                            (float(hcap_value), -1 * float(hcap_value)),
                            (data['home'], data['away']),
                            data['delta']
                        ))
            sort_arry = sorted(arry, key=lambda k: k[3], reverse=False)
            return sort_arry[0] if sort_arry[0][0] > 10 else sort_arry[1]
    except Exception:
        log_odds.exception('From hcap_totl()')


def over_under():
    pass


def get_odds(xeid, xhash):
    try:
        mp.freeze_support()
        pool = mp.Pool(processes=3)
        res = [
            pool.apply(home_away, args=(xeid, xhash,)),
            # ex. pool.apply(hcap_totl, args=(xeid, xhash, 'hcap',)),
            # ex. pool.apply(hcap_totl, args=(xeid, xhash, 'totl',))
            pool.apply(h_cap, args=(xeid, xhash, 'hcap',)),
            pool.apply(over_under, args=(xeid, xhash, 'totl',))
        ]
        pool.close()

        # check if no one is Ecxeption like [(...), (...), None]
        if None not in res:
            return res
    except Exception:
        log_odds.exception('From get_odds')

if __name__ == '__main__':
    page = get_page('INwoa3YK', 'yj4e4', 'home_away')
    print(page)
