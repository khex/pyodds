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
from libs.tabler import rows_to_dict
from libs.tabler import get_xhash_score
from libs.logger import log_main

# пока мало модулей, то их не выгодно тянуть из базы, разве что потом попробовать 'pickel'
shot = ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011',
        '2010', '2009', '2008', '2007', '2006']
leng = ['2018-2019', '2017-2018','2016-2017','2015-2016', '2014-2015',
        '2013-2014', '2012-2013', '2011-2012', '2010-2011', '2009-2010',
        '2008-2009', '2007-2008', '2006-2007', '2005-2006']

data = {
    'mlb': dict(sport='baseball',   country='usa',   league='mlb',    seas_list=shot),
    'lba': dict(sport='basketball', country='italy', league='lega-a', seas_list=leng),
    'nba': dict(sport='basketball', country='usa',   league='nba',    seas_list=leng),
    'nhl': dict(sport='hockey',     country='usa',   league='nhl',    seas_list=leng)}

args = docopt(__doc__, version='0.1')
leag = args['<leag>']
meta = data[leag]
# get first value from 'seas_list'
seas = args['<seas>'] or meta['seas_list'][0]



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
            match = rows_to_dict(bs4_tag)
            print('\n\n\n match = rows_to_dict(bs4_tag) \n\n\n')
