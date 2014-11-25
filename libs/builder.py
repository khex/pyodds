from logger import log_db

#  do 2009/2010
nba_teams = [
    ('Atlanta Hawks', 'Atlanta'),
    ('Boston Celtics', 'Boston'),
    ('Brooklyn Nets', 'Brooklyn'),
    ('Charlotte Hornets', 'Charlotte'),
    ('Chicago Bulls', 'Chicago'),
    ('Cleveland Cavaliers', 'Cleveland'),
    ('Dallas Mavericks', 'Dallas'),
    ('Denver Nuggets', 'Denver'),
    ('Detroit Pistons', 'Detroit'),
    ('Golden State Warriors', 'Golden State'),
    ('Houston Rockets', 'Houston'),
    ('Indiana Pacers', 'Indiana'),
    ('Los Angeles Clippers', 'LA Clippers'),
    ('Los Angeles Lakers', 'LA Lakers'),
    ('Memphis Grizzlies', 'Memphis'),
    ('Miami Heat', 'Miami'),
    ('Milwaukee Bucks', 'Milwaukee'),
    ('Minnesota Timberwolves', 'Minnesota'),
    ('New Orleans Pelicans', 'New Orleans'),
    ('New York Knicks', 'New York'),
    ('Oklahoma City Thunder', 'Oklahoma'),
    ('Orlando Magic', 'Orlando'),
    ('Philadelphia 76ers', 'Philadel'),
    ('Phoenix Suns', 'Phoenix'),
    ('Portland Trail Blazers', 'Portland'),
    ('Sacramento Kings', 'Sacramento'),
    ('San Antonio Spurs', 'San Antonio'),
    ('Toronto Raptors', 'Toronto'),
    ('Utah Jazz', 'Utah'),
    ('Washington Wizards', 'Washington'),
]

link_names = [
    'atlanta-hawks', 'boston-celtics', 'brooklyn-nets',
    'charlotte-hornets', 'chicago-bulls', 'cleveland-cavaliers',
    'dallas-mavericks', 'denver-nuggets', 'detroit-pistons',
    'golden-state-warriors', 'houston-rockets', 'indiana-pacers',
    'los-angeles-clippers', 'los-angeles-lakers', 'memphis-grizzlies',
    'miami-heat', 'milwaukee-bucks', 'minnesota-timberwolves',
    'new-orleans-pelicans', 'new-york-knicks', 'oklahoma-city-thunder',
    'orlando-magic', 'philadelphia-76ers', 'phoenix-suns',
    'portland-trail-blazers', 'sacramento-kings', 'san-antonio-spurs',
    'toronto-raptors', 'utah-jazz', 'washington-wizards']

def stat_line(score, line):
    try:
        if score[0] > score[1]:
            return [1, -1] if line[0] < line[1] else [2, -2]
        else:
            return [-2, 2] if line[0] < line[1] else [-1, 1]
    except Exception:
        log_db.exception('From stat line')


def get_teams(team_full):
    for team in nba_teams:
        if team_full == team[0]:
            return team
    

def profit(self):
    if self.data.score[0] > self.data.score[1]:
        return [int(round((self.data.odds[0] - 1) * 100, 2)), -100]
    else:
        return [-100, int(round((self.data.odds[0] - 1) * 100, 2))]


def handy_counter(score, handy):
    try:
        home, away = score[0]-score[1], score[1]-score[0]
        if handy[0] < handy[1]:
            return home + handy[0], away + handy[1]
        else:
            return home + handy[0], away + handy[1]
    except Exception:
        log_db.exception('From handy_counter')


def resulter(side, score):
    try:
        total = score[0] + score[1]
        if side == 'home':
            return (
                True if score[0] > score[1] else False,
                score[0] - score[1],
                total,
                score[0])
        else:
            return (
                True if score[1] > score[0] else False,
                score[1] - score[0],
                total,
                score[1])
    except Exception:
        log_db.exception('From resulter')


def itot(handy, total):
    """
    Count individual total from
    total and handyCap value

    :param
        handy: (48, (-7.5, 7.5), (1.87, 1.93), 0.06)
        total: (42, (200.5, 200.5), (1.88, 1.91), 0.03)
    :return
        (98.5, 93,5)
    """
    hand = abs(handy[1][0])
    half = (total[1][0] - abs(handy[1][0])) / 2
    if half % 1 == 0:
        if handy[1][0] < 0:
            return half + hand, half + 0.5
        else:
            return half + 0.5, half + hand
    else:
        if handy[1][0] < 0:
            return half + hand - 0.5, half
        else:
            return half, half + hand - 0.5


def builder(mdata):
    """
    Buid match results dicst()

    :param
        mdata: Match
    :return {
        'league': 'NBA',
        'links': {
            'oddsportal': 'http...san-antonio-spurs-miami-heat-67Upolsm/',
            'nba': '',
            'betxplorer': ''},
        'season': '2014/2015',
        'xeid': '67Upolsm', 
        'datetime': {
            'date': '11-06-14',
            'timestamp': 1402448400, 
            'datetime': '11 Jun 2014 04:00',
            'scraptime': '2014-11-25 13:50:44',
            'time': '04:00'}, 
        'score': {
            'score': [104, 87],
            'res_box': '22:29, 25:11, 30:18, 27:29',
            'ot': False}, 
        'away': {
            'full': 'Miami Heat',
            'short': 'Miami'},
            'profit': (0, 0, 0, 0),
            'result': (False, -17, 191, 87),
            'delta': (-1, -5.5, -9.5, -7.5), 
        'home': {... as away ... },
        'sport': 'basketball', 
        'type': 'play-offs', 
        'odds': {
            'line': (1.28, 3.65),
            'total': (200.5, 1.91, 1.91),
            'indy': ((105.5, 1.91, 1.91), (94.5, 1.91, 1.91)),
            'handy': ((-11.5, 1.92), (11.5, 1.89))}}
    """
    try:
        from datetime import datetime
        mdata['itot'] = itot(mdata['hcap'], mdata['totl'])
        datetime = {
            'date': mdata['date'],
            'time': mdata['time'],
            'datetime': mdata['datetime'],
            'timestamp': mdata['timestamp'],
            'scraptime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        score = {
            'score': mdata['score'],
            'ot': mdata['ot'],
            'res_box': mdata['res_box']}
        
        st = stat_line(mdata['score'], mdata['line'])
        hc = handy_counter(mdata['score'], mdata['hcap'][1])
        tl = (mdata['score'][0] + mdata['score'][1]) - mdata['totl'][1][0]
        it = (mdata['score'][0] - mdata['itot'][0],
              mdata['score'][1] - mdata['itot'][1])

        home = {
            'result': resulter('home', mdata['score']),
            'delta': (st[0], hc[0], tl, it[0]),
            'profit': (
                int(mdata['line'][0] * 100 - 100) if st[0] > 0 else 0,
                int(mdata['hcap'][2][0] * 100 - 100) if hc[0] > 0 else 0,
                int(mdata['totl'][2][0] * 100 - 100) if tl > 0 else 0,
                91 if it[0] > 0 else 0)}

        home['full'], home['short'] = get_teams(mdata['teams'][0])

        away = {
            'result': resulter('away', mdata['score']),
            'delta': (st[1], hc[1], tl, it[1]),
            'profit': (
                int(mdata['line'][1] * 100 - 100) if st[1] > 0 else 0,
                int(mdata['hcap'][2][1] * 100 - 100) if hc[1] > 0 else 0,
                int(mdata['totl'][2][0] * 100 - 100) if tl > 0 else 0,
                91 if it[1] > 0 else 0)}

        away['full'], away['short'] = get_teams(mdata['teams'][1])

        #  count nba link & betexplorer
        links = {
            'oddsportal': 'http://www.oddsportal.com/' + mdata['link'],
            'nba': '',
            'betxplorer': ''}

        odds = {
            'line': mdata['line'],
            'handy': (
                (mdata['hcap'][1][0], mdata['hcap'][2][0]),
                (mdata['hcap'][1][1], mdata['hcap'][2][1])),
            'total': (
                mdata['totl'][1][0], mdata['totl'][2][1], mdata['totl'][2][1]),
            'indy': (
                (mdata['itot'][0], 1.91, 1.91),
                (mdata['itot'][1], 1.91, 1.91))}

        new_match = dict(
            sport='basketball',
            league='NBA',
            season=mdata['season'],
            type=mdata['type'],
            xeid=mdata['xeid'],
            datetime=datetime,
            home=home,
            away=away,
            odds=odds,
            score=score,
            links=links)

        return new_match
    except Exception:
        log_db.exception('Builder function err')

if __name__ == '__main__':
    match_data = {
        'season': '2014/2015',
        'ot': False,
        'hash': 'yj1b4',
        'xeid': '67Upolsm',
        'type': 'play-offs',
        'score': [104, 87],
        'link': '/basketball/usa/nba-2013-2014/san-antonio-spurs-miami-heat-67Upolsm/',
        'teams': ['San Antonio Spurs', 'Miami Heat'],
        'res_box': '22:29, 25:11, 30:18, 27:29',
        'date': '11-06-14',
        'timestamp': 1402448400,
        'time': '04:00',
        'datetime': '11 Jun 2014 04:00',
        'line': (1.28, 3.65),
        'hcap': (48, (-11.5, 11.5), (1.92, 1.89), 0.03),
        'totl': (38, (200.5, 200.5), (1.9, 1.91), 0.01)}

    print builder(match_data)