#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import requests
import json
from bs4 import BeautifulSoup
from logger import log_tabler
from mdb import get_xeid


def get_table(sport, strana, liga, sezon):
    """-----------------------------------------------------------------------
        Строит адресс ссылки из аргументов и pager aka iks от 1 до 60
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
            sport, strana, liga, sezon
        Return:
            'Ok.'
    -----------------------------------------------------------------------"""
    # dublicated = 0
    seas_type = ''
    for iks in list(range(7, 8)):
        tags_list = []
        # http://www.oddsportal.com/baseball/usa/mlb-2013/results/#/page/7/
        text = 'http://www.oddsportal.com/{}/{}/{}-{}/results/#/page/{}/'
        url = text.format(sport, strana, liga, sezon, iks)
        r = requests.get(url)
        if r.status_code != 200:
            print('results page status code is {}'.format(r.status_code))
            break
        r.encoding = 'ISO-8859-1'

        """ get variable page from 'partilas\sceleton.html'
            var page = new PageTournament({
                "id":"f7RlGfit","sid":3,"cid":200,"archive":true
            });
        """
        r_string = str(r.content)
        starts = r_string.find("var page = new PageTournament") + 30
        ends = r_string.find(");var menu_open")
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
        link_1 = "http://fb.oddsportal.com/ajax-sport-country-tournament-"
        link_2 = "archive/{}/{}/X0/1/3/{}?_=1432400166447"
        ajax_link = str(link_1 + link_2).format(params["sid"], params["id"], iks)

        # requests 'r', 'q', 's', 't'
        q = requests.get(ajax_link)
        if q.status_code != 200:
            print('results page status code is {}'.format(q.status_code))
        q.encoding = 'ISO-8859-1'

        q_string = str(q.content)
        starts = q_string.find("html")
        raw_text = q_string[starts + 7:-19].replace('\\\\/', '/').replace('\\\\"', '"')
        soup = BeautifulSoup(raw_text, ["lxml", "xml"])

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
                    if game_type == "- Play Offs12B":
                        seas_type = 'play-offs'
                    elif game_type == "- Pre-season12B":
                        seas_type = 'pre-season'
                    elif game_type == "- Wild Card12B":
                        seas_type = 'wild-card'
                    elif game_type == "12B":
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
                    """"
                    # проверить матч в базе но что именно брейканетса ?
                    if get_xeid(match['xeid']):
                        log_tabler.info('{} match in Base'.format(match['xeid']))
                        break
                    """
                    # проверить матч окончен ли, что именно брейканетса ?
                    decoded = html_to_dict(tag)
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
                    }"""
                    m_xhash = match_xhash(match['link'])
                    match.update(m_xhash)

                    print(match)
                    # отправить в odds.py

            # уже не нужен, функция вернет 'Ok.'
            return tags_list


def html_to_dict(tr):
    """-----------------------------------------------------------------------
        Внутреняя вспомогательная функция, которая из ковертирует bs4 html
        таги и возвращает dict()
        Argument:
            tr => bs4 html tag
        Return: {
            'link': '/basketball/usa/ ... -miami-heat-67Upolsm/',
            'teams': ['San Antonio Spurs', 'Miami Heat'],
            'date': '11-06-14',
            'timestamp': 1402448400,
            'time': '04:00',
            'datetime': '11 Jun 2014 04:00'
        }
    -----------------------------------------------------------------------"""
    match = {}
    t_data = tr.contents

    """ score """
    # ended: class="center bold table-score table-odds"
    # live : class="center bold table-score table-odds live-score"
    if len(t_data[2].get('class')) > 35:
        return None
    else:
        match['score'] = t_data[2].text

    """   date & time   """
    try:
        #  table-time datet t1397689200-1-1-0-0
        """ добавить  GMT +3"""
        data = int(t_data[0].get('class').split(' ')[2].split('-')[0][1:])
        if not data > 1072915201:
            log_tabler.error('UTS: %s is older than Jan 2004', data)
        # 2014-06-16 03:00:00
        temp = datetime.datetime.fromtimestamp(data)
        match['timestamp'] = data
        match['datetime'] = temp.strftime("%d %b %Y %H:%M")
        match['date'] = temp.strftime("%d-%m-%y")
        match['time'] = temp.strftime("%H:%M")
    except Exception:
        log_tabler.exception('bs4.tag => date & time')

    """ teams """
    try:
        teams = str(t_data[1].find('a').text).split(' - ')
        if not len(teams) == 2 and len(teams[0]) > 3 and len(teams[0]) > 3:
            log_tabler.error("Teams is %s", teams)
            pass
        match['teams'] = teams
    except Exception:
        log_tabler.exception('bs4.tag => teams')

    """ link """
    try:
        match['link'] = str(t_data[1].find('a').get('href'))
    except Exception:
        log_tabler.exception('bs4.tag => link')
    return match


def match_xhash(arg_url):
    """-----------------------------------------------------------------------
        Идет на страницу матча, вырезает 'xhash' и развернутые результати
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
    -----------------------------------------------------------------------"""
    match = {}
    try:
        # second next 'soup' is 'borshch'
        # partilas\match_page.html 1417
        p = requests.get("http://www.oddsportal.com" + arg_url)
        p.encoding = 'ISO-8859-1'
        raw_text = str(p.content)

        """   xhash, xhashf ???? """
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

        """ score 'partials/match_score.html'   """
        try:
            borshch = BeautifulSoup(p.content)
            status = borshch.find(id='event-status')
            temp = status.find('p').get('class')[0]
            if temp == 'result':

                match['score'] = [int(x) for x in str(status.strong.text).split(' ')[0].split(':')]
                # ' (0:0, 0:3, 0:2, 0:0, 0:0, 2:0, 0:0, 0:1, 1:0)'
                match['res_box'] = str(status.p.contents[2]).replace('(', '').replace(')', '').strip()

                if len(match['res_box'].split(', ')) == 4:
                    match['ot'] = False
                else:
                    match['ot'] = True

            elif temp == 'result-alert':
                log_tabler.error('Result Alert (match was canseled)')
            else:
                log_tabler.error('There is no resullts on the match page')
        except Exception:
            log_tabler.exception('page => score')

        return match
    except Exception:
        log_tabler('Smth wrong with rows_func')

if __name__ == '__main__':
    resp = get_table('baseball', 'usa', 'mlb', '2014')
    if resp:
        print(resp[0])
    else:
        print('Empty')
    # print(match_xhash("/baseball/usa/mlb-2014/los-angeles-dodgers-san-diego-padres-r3lHy2G8/"))
