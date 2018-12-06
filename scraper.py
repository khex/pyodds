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

from docopt import docopt
from libs.tabler import get_table
from libs.rowler import rowler
from libs.tabler import get_xhash_score
from libs.logger import log_main

data = {
    'mlb': dict(sport='baseball',   country='usa',   league='mlb',    season='2018'),
    'lba': dict(sport='basketball', country='italy', league='lega-a', season='2018-2019'),
    'nba': dict(sport='basketball', country='usa',   league='nba',    season='2018-2019'),
    'nhl': dict(sport='hockey',     country='usa',   league='nhl',    season='2018-2019')}

args = docopt(__doc__, version='0.1')
leag = args['<leag>']
meta = data[leag]
# get first value from 'seas_list'
seas = args['<seas>'] or meta['season']

# if first and last page was not defined
# create it like 1 and 50
first = 1 if args['<fpage>'] is None else int(args['<fpage>'])
last = 50 if args['<lpage>'] is None else int(args['<lpage>'])

#  check if page numb arguments is correct
if last < first:
    raise Exception('First page is bigger than last!')

"""   SCRAP RESULTS PAGE   """
diapazon = range(first, last)
text = 'Start seas {} from {} to {} page'
log_main.info(text.format(seas, first, last))

"""  DO SMTH  """
tags_list = get_table(meta, seas, diapazon)

# if tags_list is not None:
if tags_list:
    print('\n\n\n if tag list \n\n\n')
    ###################
    #   row by rows   #
    ###################
    for y, tag_arr in enumerate(tags_list):
        seas_type, xeid, bs4_tag = tag_arr
        print('\n\n\n for y, tag_arr in enumerate(tags_list): \n\n\n')
        ###################
        #   check xeid    #
        ###################
        xgxs = get_xhash_score(xeid)
        if xgxs is True:
            print('Xeid: %s exist' % xeid)

        #######################
        #   match from tags   #
        #######################
        else:
            match = rowler(bs4_tag)
            print('\n\n\n match = rowler(bs4_tag) \n\n\n')
