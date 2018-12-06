#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from mongodb import teams
from logger import log_tabler

def rowler(t_data):
    """ Парсит рядки из таблицы результатов из 'bs4_html_tag' в словарь

        Arguments:
            t_data @ list of bs4 html tags: [
                <td class="table-time datet t1435975800-1-1-0-0 "/>,
                <td class="name table-participant" colspan="2">...</a></td>,
                <td class="center bold table-odds table-score">1:2</td>,
                <td class="odds-nowrp" ... xoid="E-221vlx2rrhkx0x48ku5">-</td>,
                <td class="result-ok ..." xoid="E-221vlx2rrhkx0x48ku6">-</td>,
                <td class="center info-value">14</td>]
        Return: {
            'link': '/basketball/usa/ ... -miami-heat-67Upolsm/',
            'teams': ['San Antonio Spurs', 'Miami Heat'],
            'date': {
                'date': '11-06-14',
                'timestamp': 1402448400,
                'time': '04:00',
                'datetime': '11 Jun 2014 04:00'}}
    """
    try:
        resp_dict = dict(date={}, link='', teams=[])

        """ get match link """
        resp_dict['link'] = str(t_data[1].find('a').get('href'))
        print(resp_dict['link'])
        """ partials/match_types.html
            Матч окончился 'счет:счет' либо отменен:
            - ret.   > Retired
            - postr. > Postponed
            - canc.  > Canceled
            - abn.   > Abandoned
        """
        result = t_data[2].text
        if ':' not in result:
            return '{} match was {}'.format(resp_dict['link'], result)

        """   get date & time   """
        #  table-time datet t1397689200-1-1-0-0
        date = resp_dict['date']
        ts = int(t_data[0].get('class').split(' ')[2].split('-')[0][1:])

        date['ts'] = str(ts)  # '1397689200'
        date["iso"] = datetime.datetime.fromtimestamp(ts, None)

        iso_ts = datetime.datetime.fromtimestamp(ts)
        date['date'] = iso_ts.strftime('%d-%m-%Y')  # '16-06-15'
        date['time'] = iso_ts.strftime('%H:%M')  # '03:00'
        date['datetime'] = iso_ts.strftime('%y-%m-%d %H:%M')  # '2015-06-16 03:00'

        """ get teams """
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
            raise Exception('\n\nTeam \'{}\' is not in DB\n'.format(resp_dict['teams'][0]))

        if away:
            resp_dict['tids'][1] = away['tid']
        else:
            raise Exception('\n\nTeam \'{}\' is not in DB\n'.format(resp_dict['teams'][1]))

        print(resp_dict)
        return resp_dict

    except Exception:
        log_tabler.exception('func rowler()')
