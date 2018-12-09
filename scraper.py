#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Odds portal scraper

Usage:
    scraper.py <leag> [<seas>] [<fpage> <lpage>]
    scraper.py -d | --debug
    scraper.py -v | --version
    scraper.py -h | --help

Options:
    python scraper.py nba
    python scraper.py nba 2016-2017
    python scraper.py mlb 2015
    -d --debug        Show debug messages.
    -h --help         Show this screen.
    -v --version      Show version.
"""
import sys
import json
import pprint
import requests
from docopt import docopt
from bs4 import BeautifulSoup

from libs.mongodb import matches
from libs.odds import get_odds
from libs.builder import Match
from libs.rowler import rowler
from libs.xhasher import xhasher
from libs.logger import log_main
from libs.logger import log_tabler

""" TODO
      [ ] add counter for matches in DB. if it > 5 than sys.exit()
      [ ] seas_type >> 
"""

data = {
    'mlb': dict(sport='baseball',   country='usa',   league='mlb',    seas_year='2018'),
    'lba': dict(sport='basketball', country='italy', league='lega-a', seas_year='2018-2019'),
    'nba': dict(sport='basketball', country='usa',   league='nba',    seas_year='2018-2019'),
    'nhl': dict(sport='hockey',     country='usa',   league='nhl',    seas_year='2018-2019')}

args = docopt(__doc__, version='0.1')
leag = args['<leag>']
meta = data[leag]
seas = args['<seas>'] or meta['seas_year']

# if first and last page was not defined create it like 1 and 50
first = 1 if args['<fpage>'] is None else int(args['<fpage>'])
last  = 99 if args['<lpage>'] is None else int(args['<lpage>'])

# inform on screen about pagination numbers.
text = 'Start seas {} from {} to {} page'
log_main.info(text.format(seas, first, last))

user_agnt = 'Mozilla/5.0 (Windows NT 6.1) ' +\
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +\
            'Chrome/70.0.3538.110 Safari/537.36'

for page_numb in range(first, last):
    """ write smth about 
    """
    tmpl_template = 'https://www.oddsportal.com/{}/{}/{}{}/results/#/page/{}/'
    # current .../usa/nba/... or .../usa/nba-2016-2017/...
    seas_tmpl = '' if seas in ['2018', '2018-2019'] else '-' + seas
    link = tmpl_template.format(meta['sport'], meta['country'], meta['league'], seas_tmpl, page_numb)
    print('line 65:', link)

    r = requests.get(link, headers={'User-Agent': user_agnt})

    if r.status_code != 200:
        print('results page status code is {}'.format(r.status_code))
        sys.exit()

    r.encoding = 'ISO-8859-1'
    r_string = str(r.content)

    # get some needbe data
    starts = r_string.find('var page = new PageTournament') + 30
    finish = r_string.find(');var menu_open')
    params = json.loads(r_string[starts:finish])

    # Что это за ссылка ???
    ajax_tmpl = 'https://fb.oddsportal.com/ajax-sport-country-' +\
                'tournament-archive/{}/{}/X0/1/3/{}?_=1543761020036'
    ajax_link = ajax_tmpl.format(params['sid'], params['id'], page_numb)

    # request for 'r', 'q', 's', 't'
    q = requests.get(ajax_link, headers={
        'User-Agent': user_agnt,
        # make link to match dynamicaly
        'referer': 'https://www.oddsportal.com/basketball/usa/nba/'+\
                   'philadelphia-76ers-dallas-mavericks-fL8bbADr/'})

    if q.status_code != 200:
        sys.exit('EXIT: results page status code is {}'.format(q.status_code))

    q.encoding = 'ISO-8859-1'
    q_string = str(q.content)
    starts = q_string.find('html')
    raw_text = q_string[starts + 7:-19].replace('\\\\/', '/').replace('\\\\"', '"')   
    soup = BeautifulSoup(raw_text, "lxml-xml")

    """ BeautifulSoup Logic"""
    if soup.find(id='tournamentTable').find(class_='cms'):
        sys.exit('EXIT: page haven\'t resalts table.')
    else:
        seas_type = ''
        # delete first row 'Basketball » USA » NBA'
        soup_list = soup.find('table').find_all('tr')[1:]
        for tag in soup_list:
            # here are two kind of results table rows
            #  - meta data with season type
            #  - and rows with teams and score
            clss = tag.get('class')
            # <tr class="center nob-border">
            # tabler row with meta data do define seas_type
            if clss == 'center nob-border':
                game_type = tag.find('th').text[:-3].strip()
                if game_type == '- Play Offs12B':
                    seas_type = 'play-offs'
                elif game_type == '- Pre-season12B':
                    seas_type = 'pre-season'
                elif game_type == '- Wild Card12B':
                    seas_type = 'wild-card'
                elif game_type == '- All Stars12B':
                    seas_type = 'all-stars'
                elif game_type == '12B' or game_type == '1X2B':
                    seas_type = 'season'
                else:
                    raise BaseException('Undefined season type')

            # <tr class="odd deactivate" xeid="IcGSKOQC">
            # this row goes with game results
            elif clss == ' deactivate' or clss == 'odd deactivate':
                xeid = str(tag.get('xeid'))
                # find match in DB by xeid
                if matches.find_xeid(xeid):
                    log_tabler.info('{}: match in DB'.format(xeid))
                    # The continue statement rejects all the remaining statements
                    # in the current iteration of the loop and moves the control
                    # back to the top of the loop.
                    continue

                else:
                    rows = rowler(tag.contents)
                    # check if match is finished.
                    if type(rows) is str:
                        log_tabler.info(rows)
                        continue

                    else:
                        match = {}
                        match['meta'] = meta
                        match['meta']['seas_type'] = seas_type
                        match['xeid'] = xeid
                        match.update(rows)
                        xhash_score = xhasher(match['link'], meta['sport'])
                        match.update(xhash_score)
                        match['odds'] = get_odds(meta['sport'], match['xeid'], match['xhash'] )

                        pp = pprint.PrettyPrinter(indent=2)
                        pp.pprint(match)
                        
                        m = Match(match)
                        resp = matches.save_one(m)
                        print(resp, '\n')

            else:
                # pass dummy tag data not:
                # 'center nob-border', ' deactivate' or 'odd deactivate'
                pass
