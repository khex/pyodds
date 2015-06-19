#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:/Users/qm69/Code/delta_odds/libs')

from mdb import modules
from mdb import teams

m_data = {
    "mhsh": "bbitla",  # unique
    "sport": "basketball",
    "country": "Italy",
    "league": "Lega A",
    "odd_url": ("basketball", "italy", "lega-a")
}

team_dict = [
    dict(tid=35, opid="KK6dEXeM", full="Avellino", short="avellino",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=36, opid="CMsg9VYk", full="Basket Napoli", short="basket-napoli",
         seasons=('2007-2008', '2006-2007', '2005-2006')),
    dict(tid=37, opid="4jexwVmq", full="Cantu", short="cantu",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=38, opid="dzqlXYQd", full="Capo d'Orlando", short="capo-dorlando",
         seasons=('2014-2015', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=39, opid="tQh2cMeM", full="Caserta", short="caserta",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009')),
    dict(tid=40, opid="vZoLXHUj", full="Cremona", short="cremona",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010')),
    # withpout opid
    dict(tid=41, opid="", full="Biella", short="biella",
         seasons=('2012-2013', '2011-2012', '2010-2011', '2009-2010', '2008-2009',
                  '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=42, opid="", full="Brindisi", short="brindisi",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2010-2011')),
    dict(tid=43, opid="", full="Casale Monferrato", short="casale-monferrato",
         seasons=('2011-2012')),
    dict(tid=44, opid="", full="Ferrara", short="ferrara",
         seasons=('2009-2010', '2008-2009')),
    dict(tid=45, opid="", full="Fortitudo Bologna", short="fortitudo-bologna",
         seasons=('2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=46, opid="", full="Livorno", short="Livorno",
         seasons=('2006-2007', '2005-2006')),
    dict(tid=47, opid="", full="Milano", short="milano",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=48, opid="", full="Montegranaro", short="montegranaro",
         seasons=('2013-2014', '2011-2012', '2010-2011', '2009-2010', '2008-2009',
                  '2007-2008', '2006-2007', '2012-2013')),
    dict(tid=49, opid="nB8AsBuS", full="NSB Napoli", short="nsb-napoli",
         seasons=('2009-2010', '2008-2009', '2007-2008')),
    dict(tid=50, opid="", full="Pesaro", short="pesaro ",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009', '2007-2008')),
    dict(tid=51, opid="", full="Pistoia", short="pistoia",
         seasons=('2014-2015', '2013-2014')),
    dict(tid=52, opid="", full="Reggiana", short="reggiana",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2006-2007', '2005-2006')),
    dict(tid=53, opid="", full="Reggio Calabria", short="reggio-calabria",
         seasons=('2005-2006')),
    dict(tid=54, opid="", full="Roseto", short="roseto",
         seasons=('2005-2006')),
    dict(tid=55, opid="", full="Sassari", short="sassari",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011')),
    dict(tid=56, opid="", full="Scafati", short="scafati",
         seasons=('2007-2008', '2006-2007')),
    dict(tid=57, opid="", full="Siena", short="siena",
         seasons=('2013-2014', '2012-2013', '2011-2012', '2010-2011', '2009-2010',
                  '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=58, opid="", full="Teramo", short="teramo",
         seasons=('2011-2012', '2010-2011', '2009-2010', '2008-2009', '2007-2008',
                  '2006-2007', '2005-2006')),
    dict(tid=59, opid="", full="Trento", short="trento",
         seasons=('2014-2015')),
    dict(tid=60, opid="", full="Treviso", short="treviso",
         seasons=('2011-2012', '2010-2011', '2009-2010', '2008-2009', '2007-2008',
                  '2006-2007', '2005-2006')),
    dict(tid=61, opid="", full="Udine", short="udine",
         seasons=('2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=62, opid="", full="Varese", short="varese",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=63, opid="", full="Venezia", short="venezia",
         seasons=('2014-2015', '2012-2013', '2011-2012', '2013-2014')),
    dict(tid=64, opid="", full="Virtus Bologna", short="virtus-bologna",
         seasons=('2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                  '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
    dict(tid=65, opid="", full="Virtus Roma", short="virtus-roma",
         seasons=('2010-2011', '2014-2015', '2013-2014', '2012-2013', '2011-2012',
                  '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006')),
]

m_data = modules.save_n_back(m_data)
for t in team_dict:
    t['module'] = m_data

teams.save(team_dict)
