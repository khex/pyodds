#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from logger import log_tabler


def get_next():
    """ static function only for MLB !!!
        returns list of teams for the next match
        ['New York Yankees - Seattle Mariners', ... ]
    """
    resp = []
    link = 'https://www.oddsportal.com/baseball/usa/mlb/'
    r = requests.get(link)
    if r.status_code != 200:
        print('results page status code is {}'.format(r.status_code))

    r.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(r.content))

    """ <tr> of next matches has class ['odd'] or 'None' """
    soup_list = soup.find('table').find_all('tr')
    for tag in soup_list:
        clss = tag.get('class')
        if clss == None or clss == ['odd']:
            leng = tag.contents[1].find_all('a')
            if len(leng) == 2:
                resp.append(leng[1].text.strip())

    return resp
