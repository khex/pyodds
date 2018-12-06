#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from logger import log_tabler


def xhasher(arg_url, sport):
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
