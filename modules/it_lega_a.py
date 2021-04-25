#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#   path.append("C:/Users/khex/Code/pyodds/libs")
sys.path.append('/home/khex/Code/pyodds/libs')

from mongodb import modules
from mongodb import teams

m_data = {
    "mhsh": "bbitla",  # unique
    "sport": "basketball",
    "country": "Italy",
    "league": "Lega A",
    "odd_url": ("basketball", "italy", "lega-a")
}

team_dict = [
    dict(tid=35, full="Avellino", short="avellino", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=36, full="Basket Napoli", short="basket-napoli", seasons=("2007-2008", "2006-2007", "2005-2006")),
    dict(tid=37, full="Cantu", short="cantu", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=38, full="Capo d'Orlando", short="capo-dorlando", seasons=("2014-2015", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=39, full="Caserta", short="caserta", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009")),
    dict(tid=40, full="Cremona", short="cremona", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010")),
    dict(tid=41, full="Biella", short="biella", seasons=("2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=42, full="Brindisi", short="brindisi", seasons=("2014-2015", "2013-2014", "2012-2013", "2010-2011")),
    dict(tid=43, full="Casale Monferrato", short="casale-monferrato", seasons=("2011-2012")),
    dict(tid=44, full="Ferrara", short="ferrara", seasons=("2009-2010", "2008-2009")),
    dict(tid=45, full="Fortitudo Bologna", short="fortitudo-bologna", seasons=("2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=46, full="Livorno", short="Livorno", seasons=("2006-2007", "2005-2006")),
    dict(tid=47, full="Milano", short="milano", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=48, full="Montegranaro", short="montegranaro", seasons=("2013-2014", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2012-2013")),
    dict(tid=49, full="NSB Napoli", short="nsb-napoli", seasons=("2009-2010", "2008-2009", "2007-2008")),
    dict(tid=50, full="Pesaro", short="pesaro ", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008")),
    dict(tid=51, full="Pistoia", short="pistoia", seasons=("2014-2015", "2013-2014")),
    dict(tid=52, full="Reggiana", short="reggiana", seasons=("2014-2015", "2013-2014", "2012-2013", "2006-2007", "2005-2006")),
    dict(tid=53, full="Reggio Calabria", short="reggio-calabria", seasons=("2005-2006")),
    dict(tid=54, full="Roseto", short="roseto", seasons=("2005-2006")),
    dict(tid=55, full="Sassari", short="sassari", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011")),
    dict(tid=56, full="Scafati", short="scafati", seasons=("2007-2008", "2006-2007")),
    dict(tid=57, full="Siena", short="siena", seasons=("2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=58, full="Teramo", short="teramo", seasons=("2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=59, full="Trento", short="trento", seasons=("2014-2015")),
    dict(tid=60, full="Treviso", short="treviso", seasons=("2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=61, full="Udine", short="udine", seasons=("2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=62, full="Varese", short="varese", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=63, full="Venezia", short="venezia", seasons=("2014-2015", "2012-2013", "2011-2012", "2013-2014")),
    dict(tid=64, full="Virtus Bologna", short="virtus-bologna", seasons=("2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
    dict(tid=65, full="Virtus Roma", short="virtus-roma", seasons=("2010-2011", "2014-2015", "2013-2014", "2012-2013", "2011-2012", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006")),
]


if __name__ == "__main__":

    for t in team_dict:
        t["module"] = m_data
    modules.save_one(m_data)
    teams.save_many(team_dict)
