#!/usr/bin/env python
"""
Odds portal NBA scrapper

Usage:
    scrap.py hist -s <season> [-f <first>] [-l <last>]
    scrap.py last [-l <last>]
    scrap.py -d | --debug
    scrap.py -v | --version
    scrap.py -h | --help

Options:
    -s --season         Season like '13/14'
    -f --first <first>  First page to scrap.
    -l --last <last>    Last page to scrap.
    -d --debug          Show debug messages.
    -h --help           Show this screen.
    -v --version        Show version.
"""

from docopt import docopt
from libs.tablerows import table, rows
from libs.odds import get_odds
from libs.builder import builder
from logger import log_main


seas = {'14/15': '2014-2015', '13/14': '2013-2014', '12/13': '2012-2013',
        '11/12': '2011-2012', '10/11': '2010-2011', '09/10': '2009-2010',
        '08/09': '2008-2009', '07/08': '2007-2008', '06/07': '2006-2007'}
args = docopt(__doc__, version='0.1.7')
season = seas[args['<season>']]

if args['hist'] is True:
    # if first and last page was not defined
    #  create it like 1 and 50
    first_page = 1 if args['--first'] is None else int(args['--first'])
    last_page = 50 if args['--last'] is None else int(args['--last'])

    #  check if page numb arguments is correct
    if last_page < first_page:
        raise Exception('First page is bigger than last!')

    #  check if Mongodb is avaliable
    if not mongo_avaliable():
        raise Exception('MongoDB is not avaliable!')
        #  pymongo.errors.ConnectionFailure

    #   scrap results pages
    for x in xrange(first_page, last_page):

        log_main.info('Start season %s from %s to %s page', season, first_page, last_page)
        print "---------------------------------------"
        print "| Scrap season %s from %s to %s page |" % (season, first_page, last_page)
        print "---------------------------------------\n"

        """
        get html from remote page
        shoul return list of tags like
        [('pre-season', 'pS6gVAwC', 'bs4.tag'), ...]
        """
        tags_list = table(season, x)

        if tags_list is not None:
            for tag_arr in tags_list:
                """
                don'd forget check_xeid in db
                """
                seas_type, xeid, bs4_tag = tag_arr
                #  defining the 'match' dict()
                match = rows(bs4_tag)

                if match is not None:
                    match['season'] = season
                    match['type'] = seas_type
                    match['xeid'] = xeid
                    bet_odd = get_odds(match['xeid'], match['xhash'])

                    if bet_odd is not None:
                        match['line'], match['hcap'], match['totl'] = bet_odd
                        #   build the Match
                        m = builder(match)

                        if m is not None:
                            save_to_mongo(m)

        '''
                        #  m is Exception
                        else:
                            pass
                #  odds Exception
                else:
                    pass
            #  match is Exception
            else:
                pass
        #  tags_list is Exception
        else:
            pass
        '''

#  Not 'hist'
else:
    print 'Woked ELSE statement'