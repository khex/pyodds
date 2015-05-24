delta_odds
==========

Подгрузка: листает папку "modules" с подмодулями
    sport: "baseball", "soccer"
    country: "usa", "ukr", "eng" 
    league: "mlb"
    season: True -> 2013/2014 or False -> 2014
Схема модуля:

Из tablerows.py -> func_rows()
    'link, team, date, time' запхать в 'func table()'