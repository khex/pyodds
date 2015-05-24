"""
Odds portal NBA scrapper

Usage:
    main.py hist -s <season> [-f <first>] [-l <last>]
    main.py last [-l <last>]
    main.py -d | --debug
    main.py -v | --version
    main.py -h | --help

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
from libs.logger import log_main
from libs.db import get_xeid, save_to_db


seas = {
    '14/15': '2014-2015', '13/14': '2013-2014', '12/13': '2012-2013',
    '11/12': '2011-2012', '10/11': '2010-2011', '09/10': '2009-2010',
    '08/09': '2008-2009', '07/08': '2007-2008', '06/07': '2006-2007'
}
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
    #  if not mongo_avaliable():
    #    raise Exception('MongoDB is not avaliable!')
    #       pymongo.errors.ConnectionFailure

    ###########################
    #   scrap results pages   #
    ###########################
    for x in range(first_page, last_page):

        log_main.info('Start season %s from %s to %s page', season, first_page, last_page)
        """
        get html from remote page
        shoul return list of tags like
        [('pre-season', 'pS6gVAwC', 'bs4.tag'), ...]
        """
        tags_list = table(season, x)

        if tags_list is not None:
            ###################
            #   row by rows   #
            ###################

            for y, tag_arr in enumerate(tags_list):
                seas_type, xeid, bs4_tag = tag_arr
                ###################
                #   check xeid    #
                ###################
                if get_xeid(xeid) is True:
                    print('Xeid: %s exist' % xeid)

                #######################
                #   match from tags   #
                #######################
                else:
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
                                res = save_to_db(m)
                                if res is not None:
                                    txt = '%s %s %s %s SAVED' % (season, x, y + 1, m['xeid'])
                                    log_main.info(txt)

#  last results
else:
    print('Woked ELSE statement')
