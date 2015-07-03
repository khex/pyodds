#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import requests
import datetime
from bs4 import BeautifulSoup
from mdb import teams, matches
from odds import get_odds
from builder import Match
from logger import log_tabler

""" Бизнесс логика страницы с таблицой результатов.
    По аргументам url адреса сайт загружает пустой скелет 'table_resalts.html',
    потом при помощи AJAX запроса получает HTML с данными матча ajax_resp.html
    и вставляет их в DOM дерево.
"""


def get_table(meta, diapz):
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
                'seas_list': '2014-2015'}
            sezon @ str: '2015'
            diapz @ range: range(1, 50)

        Return: list of {
            'teams': ['Venezia', 'Sassari'],
            'link': '/basketball/italy/lega-a/venezia-sassari-tGwcHwNl/',
            'xeid': 'tGwcHwNl',
            'xhash': 'yjc0b',

            'meta': {
                'season': '2014-2015',
                'league': 'lega-a',
                'country': 'italy',
                'sport': 'basketball',
                'seas_type': 'season'},

            'score': {
                'quat': ['19:21, 19:23, 22:10, 23:29, 7:17'],
                'full': '90:100',
                'main': '83:83',
                'ot': True},

            'date': {
                'timestamp': 1420399800,
                'date': '04-01-15',
                'datetime': '04 Jan 2015 21:30',
                'time': '21:30'}
            }
    """
    # usa/nba/results/#/page/2/ || usa/nba-2013-2014/results/#/page/2/
    domen = 'http://www.oddsportal.com'
    link_template = '{}/{}/{}/{}{}/results/#/page/{}/'
    """
    Если сезон не этого года, тогда '' иначе '2011-2012'
    ! переделать на димично
    """
    seas_tmpl = '' if meta['season'] in ['2015', '2014-2015'] else '-' + meta['season']
    seas_type = ''

    for iks in diapz:
        url = link_template.format(domen, meta['sport'], meta['country'],
                                   meta['league'], seas_tmpl, iks)
        print(url)
        r = requests.get(url)
        if r.status_code != 200:
            print('results page status code is {}'.format(r.status_code))
            break
        r.encoding = 'ISO-8859-1'

        r_string = str(r.content)
        starts = r_string.find('var page = new PageTournament') + 30
        ends = r_string.find(');var menu_open')
        params = json.loads(r_string[starts:ends])

        link_one = 'http://fb.oddsportal.com/ajax-sport-country-tournament-'
        link_two = 'archive/{}/{}/X0/1/3/{}?_=1432400166447'
        ajax_link = str(link_one + link_two).format(params['sid'], params['id'], iks)

        # requests 'r', 'q', 's', 't'
        q = requests.get(ajax_link)
        if q.status_code != 200:
            print('results page status code is {}'.format(q.status_code))
        q.encoding = 'ISO-8859-1'

        q_string = str(q.content)
        starts = q_string.find('html')
        raw_text = q_string[starts + 7:-19].replace('\\\\/', '/').replace('\\\\"', '"')
        soup = BeautifulSoup(raw_text, ['lxml', 'xml'])

        """ BeautifulSoup """
        if soup.find(id='tournamentTable').find(class_='cms'):
            """ partials/no_data.py """
            log_tabler.error('Page haven\'t resalts table')
        else:
            soup_list = soup.find('table').find_all('tr')

            for tag in soup_list[1:]:
                clss = tag.get('class')

                # 'center nob-border' Season data
                if clss == 'center nob-border':
                    game_type = tag.find('th').text[:-3].strip()
                    if game_type == '- Play Offs12B':
                        seas_type = 'play-offs'
                    elif game_type == '- Pre-season12B':
                        seas_type = 'pre-season'
                    elif game_type == '- Wild Card12B':
                        seas_type = 'wild-card'
                    elif game_type == '12B':
                        seas_type = 'season'
                    else:
                        seas_type = 'undefined'

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

                    decoded = rows_to_dict(tag.contents)
                    # проверить окончен ли матч
                    if decoded == 'unfished':
                        log_tabler.warn('{} match not fished'.format(match['xeid']))
                        continue

                    match.update(decoded)
                    xhash_score = get_xhash_score(match['link'], meta['sport'])
                    match.update(xhash_score)

                    match['odds'] = get_odds(meta['sport'], match['xeid'], match['xhash'])

                    m = Match(match)
                    resp = matches.save_one(m)
                    print(resp)

            return('Well done.')


def rows_to_dict(t_data):
    """ Парсит рядки из таблицы результатов
        с 'bs4_html_tag' в словарь

        Arguments:
            t_data => bs4 html tag

        Return: {
            'link': '/basketball/usa/ ... -miami-heat-67Upolsm/',
            'teams': ['San Antonio Spurs', 'Miami Heat'],
            'date': {
                'date': '11-06-14',
                'timestamp': 1402448400,
                'time': '04:00',
                'datetime': '11 Jun 2014 04:00'}
            }
    """
    resp_dict = dict(date={}, link='', teams=[])
    """   get date & time   """
    try:
        """
        ЭСЛИ МАТЧ НЕ ОКОНЧЕН ИЛИ ОТМЕНЕН
        return 'unfished'
        """
        #  table-time datet t1397689200-1-1-0-0
        date = resp_dict['date']
        data = int(t_data[0].get('class').split(' ')[2].split('-')[0][1:])
        date['timestamp'] = data
        # 2014-06-16 03:00:00
        temp = datetime.datetime.fromtimestamp(data)
        date['date'] = temp.strftime('%d %b %Y')
        date['time'] = temp.strftime('%H:%M')
        date['datetime'] = temp.strftime('%d-%m-%y %H:%M')
        # date['datetime'] = temp.strftime('%d %b %Y %H:%M')

    except Exception:
        log_tabler.exception('bs4.tag => date & time\n')

    """   get teams   """
    try:
        # <a href="/basketball/italy/lega-a/capo-dorlando-milano-dzzJsnCt/">
        #     <span class="bold">Capo d'Orlando</span> - Milano
        # </a>
        resp_dict['teams'] = str(t_data[1].find('a').text.replace("\\'", "'")).split(' - ')

        # проверить наличие команды в БД и выкинуть ошипку
        resp_dict['tids'] = [0, 0]
        home = teams.find_one(resp_dict['teams'][0])
        away = teams.find_one(resp_dict['teams'][1])

        if home:
            resp_dict['tids'][0] = home['tid']
        else:
            raise Exception('Team \'{}\' not in DB'.format(resp_dict['teams'][0]))

        if away:
            resp_dict['tids'][1] = away['tid']
        else:
            raise Exception('Team \'{}\' not in DB'.format(resp_dict['teams'][1]))

    except Exception:
        log_tabler.exception('bs4.tag => teams\n')

    """   get match link """
    try:
        resp_dict['link'] = str(t_data[1].find('a').get('href'))
    except Exception:
        log_tabler.exception('bs4.tag => link\n')

    return resp_dict


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
            'xhash': 'yj84d'
        }
    """
    resp_dict = dict(score={})
    try:
        # partilas\match_page.html 1417
        p = requests.get('http://www.oddsportal.com' + arg_url)
        p.encoding = 'ISO-8859-1'
        raw_text = str(p.content)

        """ xhash, xhashf <- нужен ли? """
        try:
            # возмодно нужно в JSON как в tabler ?
            frst = raw_text.find('xhash') + 8
            last = raw_text.find('xhashf') - 3
            # first hash temp var
            fhash = ''.join(raw_text[frst:last].split('%')[1:])
            xhash = bytes.fromhex(fhash).decode('utf-8')

            resp_dict['xhash'] = xhash

        except Exception:
            log_tabler.exception('page => xhash')

        """ score 'partials/match_score.html'  """
        try:
            soup = BeautifulSoup(p.content)
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

            # <p class="result-alert"><span class="bold">postponed</span></p>
            elif mtch_rslt == 'result-alert':
                log_tabler.info('Result Alert (match was canseled)')
            else:
                raise BaseException('Smth with Score scrapper')

        except Exception:
            print('\n{}\n'.format(text))
            log_tabler.exception('page => score')

        return resp_dict

    except Exception:
        log_tabler('Smth wrong with rows_func')

if __name__ == '__main__':

    modl_list = dict(sport='baseball', country='usa',
                     league='mlb', season='2015')
    diapazon = range(1, 50)
    resp = get_table(modl_list, diapazon)
    print(resp)
