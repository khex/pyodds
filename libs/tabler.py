#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/khex/Code/pyodds/libs')

import re
import json
import pprint
import requests
from bs4 import BeautifulSoup
from mongodb import teams
from mongodb import matches
from odds import get_odds
from builder import Match
from logger import log_tabler

from rowler import rowler
""" Бизнесс логика страницы с таблицой результатов.
    По аргументам url адреса сайт загружает пустой скелет 'table_resalts.html',
    потом при помощи AJAX запроса получает HTML с данными матча ajax_resp.html
    и вставляет их в DOM дерево.
"""


def get_table(meta, meta_seas, diapz):
    """ Строит адресс ссылки из аргументов и заданого диапазона.
        Идет на страницу с таблицой результатов, где фильтрует
        "table rows" только с матчем и создает массив из данных с классами:
            'even deactivate' и ' deactivate' => данные матча
            'center nob-border' => данные про сезон
            убирает: '', 'table-dummyrow', 'dark center'
        Итерирует по массиву и если матч окончен и не находится в безе данных
        передает его в 'odds.py' или по окончании возращает 'Well done.'

        Arguments:
            module @ dict: {
                'sport': 'basketball',
                'country': 'italy',
                'league': 'lega-a',
                'seas_list': '2014-2015'
            }
            sezon @ str: '2015'
            diapz @ range: range(1, 50)

        Return: ???
    """
    # usa/nba/results/#/page/2/ || usa/nba-2013-2014/results/#/page/2/
    
    """
    Если сезон не этого года, тогда '' иначе '2011-2012'
    ! переделать на димично
    """
    # нюанс ссылки: если это теперешний сезон - то год не нужно ставить
    seas_tmpl = '' if meta_seas in ['2018', '2018-2019'] else '-' + meta_seas
    seas_type = ''

    for iks in diapz:
        domen = 'https://www.oddsportal.com'
        tmpl_template = '{}/{}/{}{}/results/#/page/{}/'
        url = tmpl_template.format(meta['sport'], meta['country'], meta['league'], seas_tmpl, iks)

        # https://stackoverflow.com/questions/33350956/why-python-requests-get-a-404-error
        link = 'https://www.oddsportal.com/' + url

        proxy = {'http': 'http://www.oddsportal.com/' + url}
        r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})

        if r.status_code != 200:
            print('results page status code is {}'.format(r.status_code))
            sys.exit()
        r.encoding = 'ISO-8859-1'

        r_string = str(r.content)
        starts = r_string.find('var page = new PageTournament') + 30
        ends = r_string.find(');var menu_open')
        params = json.loads(r_string[starts:ends])
        print(params)

        # Что єто за ссілка ???
        tmpl_one = 'https://fb.oddsportal.com/ajax-sport-country-tournament-'
        tmpl_two = 'archive/{}/{}/X0/1/3/{}?_=1543761020036'
        ajax_link = str(tmpl_one + tmpl_two).format(params['sid'], params['id'], iks)
        print(ajax_link)

        # requests 'r', 'q', 's', 't'
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'referer': 'https://www.oddsportal.com/basketball/usa/nba/philadelphia-76ers-dallas-mavericks-fL8bbADr/'
        }
        q = requests.get(ajax_link, headers=headers)

        if q.status_code != 200:
            print('results page status code is {}'.format(q.status_code))
        q.encoding = 'ISO-8859-1'

        q_string = str(q.content)
        starts = q_string.find('html')
        raw_text = q_string[starts + 7:-19].replace('\\\\/', '/').replace('\\\\"', '"')
        
        soup = BeautifulSoup(raw_text, "lxml-xml")

        """ BeautifulSoup """
        if soup.find(id='tournamentTable').find(class_='cms'):
            """ partials/no_data.py """
            log_tabler.error('Page haven\'t resalts table')
        else:
            soup_list = soup.find('table').find_all('tr')

            # why slise ???
            for tag in soup_list[1:]:
                clss = tag.get('class')

                # 'center nob-border' Season data
                if clss == 'center nob-border':
                    game_type = tag.find('th').text[:-3].strip()
                    print(game_type)
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

                # 'odd deactivate', ' deactivate'
                elif clss == ' deactivate' or clss == 'odd deactivate':

                    match = {}
                    match['meta'] = meta
                    match['meta']['seas_type'] = seas_type

                    match['xeid'] = str(tag.get('xeid'))

                    # проверить наличие матча в базе
                    # 2015-06-23 20:57:16,971 INFO tabler 40wRuQtg match in Base
                    if matches.find_xeid(match['xeid']):
                        log_tabler.info('{} match in Base'.format(match['xeid']))
                        # Оператор continue начинает следующий проход цикла,
                        # минуя оставшееся тело цикла (for или while)
                        continue

                    decoded = rowler(tag.contents)
                    # проверить окончен ли матч
                    if type(decoded) is str:
                        log_tabler.info(decoded)
                        continue

                    match.update(decoded)
                    xhash_score = get_xhash_score(match['link'], meta['sport'])
                    match.update(xhash_score)
                    
                    print( meta['sport'], match['xeid'], match['xhash'] )

                    match['odds'] = get_odds(meta['sport'], match['xeid'], match['xhash'] )

                    pp = pprint.PrettyPrinter(indent=2)
                    pp.pprint(match)
                    
                    m = Match(match)

                    resp = matches.save_one(m)
                    print(resp, '\n')

                else:
                    pass

            print('Page done.')
    return('Well Done')


def get_xhash_score(arg_url, sport):
    """ Идет на страницу матча, вырезает 'xhash'
        и парсит развернутые результати

        Arguments:
            match_url '/basketball/usa/ ... -miami-heat-67Upolsm/'
            score: 'basketball'

        Return: {
            'score': {
                'main': '67:67',
                'ot': True,
                'quat': ['11:18, 19:12, 18:21, 19:16, 9:8'],
                'full': '76:75'},
            'xhash': 'yj84d'}
    """
    try:
        resp_dict = dict(score={})

        # partilas\match_page.html 1417
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'referer': 'https://www.oddsportal.com/basketball/usa/nba/philadelphia-76ers-dallas-mavericks-fL8bbADr/'
        }
        p = requests.get('https://www.oddsportal.com' + arg_url, headers=headers)
        p.encoding = 'ISO-8859-1'
        raw_text = str(p.content)

        """ xhash, xhashf <- нужен ли? """
        # возмодно нужно в JSON как в tabler ?
        frst = raw_text.find('xhash') + 8
        last = raw_text.find('xhashf') - 3
        # first hash temp var
        fhash = ''.join(raw_text[frst:last].split('%')[1:])
        xhash = bytes.fromhex(fhash).decode('utf-8')

        resp_dict['xhash'] = xhash

        """ score 'partials/match_score.html'  """
        soup = BeautifulSoup(p.content, 'lxml')
        html = soup.find(id='event-status')
        text = html.text.replace(u'\xa0', u' ')

        #  <p class="result">
        mtch_rslt = html.find('p').get('class')[0]
        score = resp_dict['score']
        if sport == 'basketball':
            if re.search('OT', text):
                score['ot'] = True
                score['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
                # ['115:115', '27:25, 17:25, 21:25, 30:20, 13:0']
                re_find = re.findall('\(([\d+:\d+,*\s*]+)\)', text)
                score['main'] = re_find[0]  # '115:115'
                # '27:25, 17:25, 21:25, 30:20, 13:0'
                score['quat'] = re_find[1]
            else:
                score['ot'] = False
                score['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
                score['quat'] = re.findall('\((.+)\)', text)

        elif sport == 'baseball':
            # "Final result 1:2 (0:0, 0:0, 0:1, 1:0, 0:0, 0:0, 0:0, 0:0, 0:0, 0:1)"
            # "Final result 5:3 (0:0, 0:0, 0:0, 0:0, 0:0, 0:0, 1:1, 4:0, X:2)"
            score['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]  # '1:2'
            score['quat'] = re.findall('\(([X:\d+,*\s*]+)\)', text)[0]
            score['ot'] = False if len(score['quat'].split(', ')) == 9 else True

        elif sport == 'hockey':
            # "Final result 3:2 (1:0, 0:2, 2:0)"
            # "Final result 5:4 OT (0:1, 3:0, 1:3, 1:0)"
            # "Final result 2:1 penalties (1:0, 0:1, 0:0, 0:0, 2:0)"
            score['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]  # '1:2'
            score['quat'] = re.findall('\(([X:\d+,*\s*]+)\)', text)[0]  # ???
            score['ot'] = False if len(score['quat'].split(', ')) == 9 else True

        # <p class="result-alert"><span class="bold">postponed</span></p>
        elif mtch_rslt == 'result-alert':
            log_tabler.info('Result Alert (match was canseled)')
        else:
            raise BaseException('Smth with Score scrapper')

        return resp_dict

    except Exception:
        log_tabler('Func get_xhash_score()')


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

if __name__ == '__main__':
    modl_list = dict(sport='hockey', country='usa', league='nhl', season='2015-2016')
    # modl_list = dict(sport='baseball', country='usa', league='mlb', season='2015')
    # modl_list = dict(sport='baseball', country='japan', league='npb', season='2015')
    diapazon = range(1, 50)
    resp = get_table(modl_list, '2018-2019', diapazon)
    print(resp)
