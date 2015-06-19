#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import requests
import datetime
from bs4 import BeautifulSoup
from mdb import matches, teams
from logger import log_tabler

""" Описание самой бизнес логики страницы результатов.
По аргументам url адреса сайт загружает пустой скелет 'table_resalts.html'.
А дальше при помощи AJAX запроса получает HTML с данными матча ajax_resp.html
"""


def get_table(module, sezon, diapz):
    """ Строит адресс ссылки из аргументов и pager aka iks от 1 до 60
        идет на страницу результатов где фильтрует из ~ 160 table rows
        только 50 шт. и создает массив из данных с классами:
            'even deactivate' и ' deactivate' => данные матча
            'center nob-border' => данные про сезон
            убирает: '', 'table-dummyrow', 'dark center'
        Итерирует по массиву и если матч окончен и не находится в безе данных
        передает его в 'odds.py' который вытягивает кф.
        дальше в 'counter.py' выщитывает дельту
        сохраняет в Монге и возращает 'Ok.' по окончании.
        Arguments:
            module @ list  => ('baseball', 'usa', 'mlb')
            sezon  @ str   => '2015'
            diapz  @ range => range(1, 50)
        Return:
            str => 'Well done.'
    """
    sport, strana, liga, ses_num = module
    # oddsportal.com/basketball/usa/nba/results/#/page/2/
    # oddsportal.com/basketball/usa/nba-2013-2014/results/#/page/2/
    domen = 'http://www.oddsportal.com'
    link_template = '{}/{}/{}/{}{}/results/#/page/{}/'
    season = '' if sezon == 0 else '-' + ses_num[sezon]
    seas_type = ''

    for iks in diapz:
        url = link_template.format(domen, sport, strana, liga, season, iks)
        r = requests.get(url)
        if r.status_code != 200:
            print('results page status code is {}'.format(r.status_code))
            break
        r.encoding = 'ISO-8859-1'

        """ get variable page from 'partilas\sceleton.html'
            var page = new PageTournament({
                'id':'f7RlGfit','sid':3,'cid':200,'archive':true
            });
        """
        r_string = str(r.content)
        starts = r_string.find('var page = new PageTournament') + 30
        ends = r_string.find(');var menu_open')
        params = json.loads(r_string[starts:ends])

        """ build Url
            http://fb.oddsportal.com/ajax-sport-country-tournament-archive/
            3/f7RlGfit/X0/1/3/7/?_=1432400166447
            var request = new Request(
                '/ajax-sport-country-tournament-archive/' +
                this.params.sid + '/'            = 3
                this.params.id + '/' +
                globals.getBookieHash() + '/' +  = X0 всегда
                usePremium + '/' +               = 1 всегда
                globals.timezoneOffset + '/' +   = UTC + 3
                pageNr + '/'                     = 1 .. 50
            );
        """
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
                    """
                    - get_xhash
                    - get_odds
                    - counter
                    - сохранить в массив
                    """
                    match = {}
                    match['season'] = seas_type
                    match['xeid'] = str(tag.get('xeid'))
                    """
                    # проверить матч в базе но что именно брейканетса ?
                    if get_xeid(match['xeid']):
                        log_tabler.info('{} match in Base'.format(match['xeid']))
                        break
                    """
                    # проверить матч окончен ли, что именно брейканетса ?
                    decoded = rows_to_dict(tag.contents)
                    if decoded == 'This is unfished match':
                        log_tabler.warn('{} match not fished'.format(match['xeid']))
                        break

                    match.update(decoded)
                    """ {
                        'date': '10-09-14',
                        'link': '/baseball/usa/mlb-2014/los-angeles-dodgers-san-diego-padres-r3lHy2G8/',
                        'datetime': '10 Sep 2014 05:10',
                        'time': '05:10',
                        'score': '3:6',
                        'season': 'season',
                        'xeid': 'r3lHy2G8',
                        'teams': ['Los Angeles Dodgers', 'San Diego Padres'],
                        'timestamp': 1410315000
                    } """
                    if not matches.get_xeid(match['xeid']):
                        break
                    m_xhash = get_xhash_n_score(match['link'], sport)
                    match.update(m_xhash)

                    # отправить match в odds.py
                    # print(match)

            return('Well done.')


def rows_to_dict(t_data):
    """
        бившый func rows()
        Внутреняя вспомогательная функция, которая из ковертирует bs4 html
        таги и возвращает dict()
        Argument:
            t_data => bs4 html tag
        Return: {
            'link': '/basketball/usa/ ... -miami-heat-67Upolsm/',
            'teams': ['San Antonio Spurs', 'Miami Heat'],
            'date': '11-06-14',
            'timestamp': 1402448400,
            'time': '04:00',
            'datetime': '11 Jun 2014 04:00'
        }
    """
    match = {}
    """   get date & time   """
    try:
        #  table-time datet t1397689200-1-1-0-0
        data = int(t_data[0].get('class').split(' ')[2].split('-')[0][1:])
        match['timestamp'] = data
        # 2014-06-16 03:00:00
        temp = datetime.datetime.fromtimestamp(data)
        match['datetime'] = temp.strftime('%d %b %Y %H:%M')
        match['date'] = temp.strftime('%d-%m-%y')
        match['time'] = temp.strftime('%H:%M')
    except Exception:
        log_tabler.exception('bs4.tag => date & time\n')

    """   get teams   """
    try:
        # <a href="/basketball/italy/lega-a/capo-dorlando-milano-dzzJsnCt/">
        #     <span class="bold">Capo d'Orlando</span> - Milano
        # </a>
        # 'Capo d'Orlando - Milano'
        match['teams'] = str(t_data[1].find('a').text.replace("\\'", "'")).split(' - ')
        home, away = match['teams']
        if teams.find(home):
            print('Team {} in DB'.format(home))
        if not teams.find(away):
            print('Team {} not in DB'.format(away))

    except Exception:
        log_tabler.exception('bs4.tag => teams\n')

    """   get match link """
    try:
        match['link'] = str(t_data[1].find('a').get('href'))
    except Exception:
        log_tabler.exception('bs4.tag => link\n')

    return match


def get_xhash_n_score(arg_url, sport):
    """
        Идет на странице матча, вырезает 'xhash' и развернутые результати
        - xhash (нужен для JSON запросов коеф. в 'odds.py')
        - Final result: ('22:29, 25:11, 30:18, 27:29')

        Arguments
            match_url '/basketball/usa/ ... -miami-heat-67Upolsm/'
        Return {
            'ot': False,
            'xhash': 'yj1b4',
            'score': [104, 87],
            'res_box': '22:29, 25:11, 30:18, 27:29',
        }
    """
    match = {}
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
            if len(xhash) != 5:
                log_tabler.error('page => xhash is %s', xhash)
                return AssertionError('ASSERT: xhash is ', xhash)
            match['xhash'] = xhash
        except Exception:
            log_tabler.exception('page => xhash')

        """ score 'partials/match_score.html'  """
        try:
            soup = BeautifulSoup(p.content)
            html = soup.find(id='event-status')
            text = html.text.replace(u'\xa0', u' ')

            #  <p class="result">
            mtch_rslt = html.find('p').get('class')[0]
            if mtch_rslt == 'result':
                if sport == 'basketball':
                    if re.search('OT', text):
                        match['ot'] = True
                        match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
                        # ['115:115', '27:25, 17:25, 21:25, 30:20, 13:0']
                        re_find = re.findall('\(([\d+:\d+,*\s*]+)\)', text)
                        # '115:115'
                        match['main'] = re_find[0]
                        # ['27:25, 17:25, 21:25, 30:20, 13:0']
                        match['quat'] = re_find[1:]
                    else:
                        match['ot'] = False
                        match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
                        match['quat'] = re.findall('\((.+)\)', text)
                elif sport == 'baseball':
                    match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
                    match['quat'] = re.findall('\(([\d+:\d+,*\s*]+)\)', text)[0]
                    match['ot'] = False if len(match['quat'].split(', ')) == 9 else True
            # <p class="result-alert"><span class="bold">postponed</span></p>
            elif mtch_rslt == 'result-alert':
                log_tabler.info('Result Alert (match was canseled)')
            else:
                log_tabler.error('There is no resullts')
        except Exception:
            log_tabler.exception('page => score')

        return match

    except Exception:
        log_tabler('Smth wrong with rows_func')

if __name__ == '__main__':
    modl_list = ('basketball', 'italy', 'lega-a', ['2014-2015', '2013-2014', '2012-2013'])
    diapazon = range(2, 3)
    resp = get_table(modl_list, 0, diapazon)
    # print(resp)
