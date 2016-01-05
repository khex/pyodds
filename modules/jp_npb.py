#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/qm69/Code/delta_odds/libs')

from mongodb import modules
from mongodb import teams

m_data = dict(mhsh="bsjpnp",  # доцільність
              sport="baseball",
              country="Japan",
              league="NPB",
              odd_url=("baseball", "japan", "npb"))

year = ['2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008']

team_dict = [
    dict(tid=100, seasons=year, full="Chiba Lotte Marines", short='Chiba', link="chiba-lotte-marines"),
    dict(tid=101, seasons=year, full="Chunichi Dragons", short='Chunichi', link="chunichi-dragons"),
    dict(tid=102, seasons=year, full="Fukuoka S. Hawks", short='Fukuoka', link="fukuoka-s-hawks"),
    dict(tid=103, seasons=year, full="Hanshin Tigers", short='Hanshin', link="hanshin-tigers"),
    dict(tid=104, seasons=year, full="Hiroshima Carp", short='Hiroshima', link="hiroshima-carp"),
    dict(tid=105, seasons=year, full="Nippon Ham Fighters", short='Nippon', link="nippon-ham-fighters"),
    dict(tid=106, seasons=year, full="Orix Buffaloes", short='Orix', link="orix-buffaloes"),
    dict(tid=107, seasons=year, full="Rakuten Gold. Eagles", short='Rakuten', link="rakuten-gold-eagles"),
    dict(tid=108, seasons=year, full="Seibu Lions", short='Seibu', link="seibu-lions"),
    dict(tid=109, seasons=year, full="Yakult Swallows", short='Yakult', link="yakult-swallows"),
    dict(tid=110, seasons=year, full="Yokohama Baystars", short='Yokohama', link="yokohama-baystars"),
    dict(tid=111, seasons=year, full="Yomiuri Giants", short='Yomiuri', link="yomiuri-giants")
]

if __name__ == '__main__':

    for t in team_dict:
        t['module'] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
