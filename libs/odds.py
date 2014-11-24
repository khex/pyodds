import json
import requests
import multiprocessing as mp
from bs4 import BeautifulSoup
from logger import log_odds


pref = 'http://fb.oddsportal.com/feed/match/'
decoder = json.JSONDecoder(object_hook=None, parse_float=None, parse_int=None,
                           parse_constant=None, strict=True, object_pairs_hook=None)


def get_page(xeid, xhash, match_type):
    """
    Helper func to line() & hcap_totl()
    that recieve JSON from remote oddsportal
    1-3-UX19OwXR-5-1-yja8d.dat?_=1415473715925
    1-3-UX19OwXR-3-1-yja8d.dat?_=1415473649648
    1-3-UX19OwXR-2-1-yja8d.dat?_=1415473649648

    :param
        xeid:
        xhash:
        match_type: 'line', 'hcap', 'total'
    :return {  'E-3-1--3.5-0-0': ..,
               'E-3-1-1.5-0-0': ...,  }
    """
    try:
        type_dict = {'line': '-3-1-', 'hcap': '-5-1-', 'totl': '-2-1-'}
        link = pref + '1-3-' + xeid + type_dict[match_type] + xhash + '.dat'
        r = requests.get(link)
        #globals.jsonpCallback('/feed/match/1-3-UX19OwXR-3-1-yja8d.dat',
        #);
        json_string = str(r.content)[63:-2]
        dic_obj = decoder.decode(json_string)
        return dic_obj['d']['oddsdata']['back'] 
    except Exception:
        log_odds.exception('From: get_rage()')


def map_odds(odds_arry):
    """
    Helper func to line() & hcap_totl() that

    :param
        odds_arry: {
            'E-3-1--3.5-0-0': ... , }
    :return {
        'length': 48,
        'home': 1.85,
        'away': 1.93,
        'delta': .08, }
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


def line(xeid, xhash):
    """
    Get values of line odds

    :param
        xeid:  '67Upolsm'
        xhash: 'yj1b4'
    :return
        (1.27, 2.55)
    """
    try:
        odds_dict = get_page(xeid, xhash, 'line')['E-3-1-0-0-0']['odds']
        if odds_dict is not None:
            odds_arry = [odds_dict[item] for item in odds_dict]
            data = map_odds(odds_arry)
            if data is not None:
                return data['home'], data['away']
    except Exception:
        log_odds('From line_func()')


def hcap_totl(xeid, xhash, odd_type):
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

def get_odds(xeid, xhash):
    try:
        mp.freeze_support()
        pool = mp.Pool(processes=3)
        res = [
            pool.apply(line, args=(xeid, xhash,)),
            pool.apply(hcap_totl, args=(xeid, xhash, 'hcap',)),
            pool.apply(hcap_totl, args=(xeid, xhash, 'totl',))
        ]
        pool.close()

        # check if no one is Ecxeption like [(...), (...), None]
        if None not in res:
            return res
    except Exception:
        log_odds.exception('From get_odds')

if __name__ == '__main__':
    full = 'http://www.oddsportal.com/basketball/usa/nba/'
    url = [
        'golden-state-warriors-san-antonio-spurs-WbTfeRfO/',
        'portland-trail-blazers-charlotte-hornets-lzvjd7uI/',
        'dallas-mavericks-sacramento-kings-AquncmQB/',
        'memphis-grizzlies-los-angeles-lakers-OStva9ea/',
        'milwaukee-bucks-oklahoma-city-thunder-2JurbTA5/',
        'toronto-raptors-orlando-magic-E743z0hn/',
        'los-angeles-clippers-san-antonio-spurs-t4iZaktg/',
        'chicago-bulls-detroit-pistons-S0mV0VQn/',
        'new-york-knicks-atlanta-hawks-YwlR1BBt/',
        'cleveland-cavaliers-new-orleans-pelicans-KdsFff4D/',
        'indiana-pacers-utah-jazz-dEQcJwsE/',
        'los-angeles-lakers-charlotte-hornets-t6rBezk7/',
        'portland-trail-blazers-denver-nuggets-nqq7dGZ0/',
        'phoenix-suns-golden-state-warriors-z9u3cdKf/',
        'dallas-mavericks-miami-heat-hpjbbx5l/',
        'oklahoma-city-thunder-sacramento-kings-EgifaIkr/',
        'toronto-raptors-philadelphia-76ers-040aytwt/',
        'detroit-pistons-utah-jazz-M1aS3bsR/',
        'brooklyn-nets-orlando-magic-rB0O4vSK/',
        'milwaukee-bucks-memphis-grizzlies-nq7F60c8/',
        'san-antonio-spurs-new-orleans-pelicans-0nBJ5KCE/',
        'chicago-bulls-boston-celtics-fkKTrc51/',
        'houston-rockets-golden-state-warriors-YuJXsHK7/',
        'atlanta-hawks-new-york-knicks-lxkTpJzk/',
        'miami-heat-minnesota-timberwolves-SSmXqwje/',
        'indiana-pacers-washington-wizards-fFkPoaLr/',
        'los-angeles-clippers-portland-trail-blazers-IgbcjuDR/',
        'denver-nuggets-cleveland-cavaliers-zV8hiLcL/',
        'phoenix-suns-sacramento-kings-S45pgsT8/',
        'utah-jazz-dallas-mavericks-dvAlh1rF/',
        'oklahoma-city-thunder-memphis-grizzlies-lE6tfND2/',
        'boston-celtics-indiana-pacers-zZOgWJLe/',
        'brooklyn-nets-new-york-knicks-tCPkXa6k/',
        'detroit-pistons-milwaukee-bucks-n9ScVwy2/',
        'toronto-raptors-washington-wizards-zsZhGd7U/',
        'charlotte-hornets-atlanta-hawks-rypFw2TL/',
        'orlando-magic-minnesota-timberwolves-MRrJxMrS/',
        'philadelphia-76ers-chicago-bulls-2LQoYuiq/',
        'portland-trail-blazers-dallas-mavericks-lEpBvrEF/',
        'houston-rockets-san-antonio-spurs-zBt7uOb9/',
        'golden-state-warriors-los-angeles-clippers-hni2t4q3/',
        'sacramento-kings-denver-nuggets-EehbspUd/',
        'phoenix-suns-memphis-grizzlies-8b5CJtxj/',
        'utah-jazz-cleveland-cavaliers-nk4GI0id/',
        'san-antonio-spurs-atlanta-hawks-QZF7KMMq/',
        'milwaukee-bucks-chicago-bulls-fiPyQraM/',
        'washington-wizards-indiana-pacers-lEOuP2ES/',
        'boston-celtics-toronto-raptors-djzkHxhO/',
        'brooklyn-nets-minnesota-timberwolves-bPVSR4U9/',
        'detroit-pistons-new-york-knicks-G0QXQOqG/',
    ]
    
    for i, u in enumerate(url):
        if i < 50:
            xeid = u[-9:][0:8]  # get xeid from link
            #print full + u
            p = requests.get(full + u)
            poup = BeautifulSoup(p.content)
            text = str(poup)
            frst = text.find('xhash') + 8
            last = text.find('xhashf') - 3
            xhash = str(text[frst:last])

            print i+1, get_odds(xeid, xhash)