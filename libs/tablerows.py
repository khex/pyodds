import datetime
import requests
from bs4 import BeautifulSoup
from logger import log_rows, log_table

#  http://stackoverflow.com/questions/9264763
link = ['http://www.oddsportal.com', '/basketball/usa/nba-', '/results/page/']


def table(season, iks):
    """
    Build url of results page, get html_page,
    filter table rows with class=(even deactivate)
        results: ['even', 'deactivate'], ['', 'deactivate'],
        season type: ['center', 'nob-border']
    unfilter: [], ['table-dummyrow'], ['dark', 'center']
    buid list of ('pre-season', bs4.tag)

    :param:
        seas_arg: str like '10/11'
        iks: int number of results page from xrange(1, 50)
    :return:
        tags_list: [('pre-season', 'pS6gVAwC', bs4.tag), ...]
    """
    try:
        seas_type, tags_list = '', []
        url = link[0] + link[1] + season + link[2] + str(iks) + '/'
        r = requests.get(url)

        if r.status_code != 200:
            log_table.error('results page status code is %s' % str(r.status_code))

        r.encoding = 'ISO-8859-1'
        soup = BeautifulSoup(r.content)

        if soup.find(id='tournamentTable').find(class_='cms'):
            log_table.error('Page haven\'t resalts table')

        else:
            soup_list = soup.find(id='tournamentTable').find('tbody').contents
            #  from 115 items to ~60
            filt_soup = filter(lambda x: len(x.get('class')) == 2, soup_list)
            for tag in filt_soup[1:]:
                if tag.get('class')[1] == 'deactivate':
                    xeid = str(tag.get('xeid'))
                    tags_list.append((seas_type, xeid, tag))
                else:
                    tayp = str(tag.contents[0].text)
                    if tayp == '':
                        seas_type = 'season'
                    elif tayp == ' - Play Offs':
                        seas_type = 'play-offs'
                    elif tayp == ' - Pre-season':
                        seas_type = 'pre-season'
                    else:
                        seas_type = "undefined"
            return tags_list
    except Exception:
        log_table.exception('Smth wrong in table_func')


def rows(tr):
    """
    Scrap data from html of table rows

    :param
        tr: bs4.tag
    :return
        match = {
            'link': '/basketball/usa/nba-2013-2014/san-antonio-spurs-miami-heat-67Upolsm/',
            'teams': ['San Antonio Spurs', 'Miami Heat'],
            'ot': False,
            'xhash': 'yj1b4',
            'tipe': 'play-offs',
            'score': [104, 87],
            'res_box': '22:29, 25:11, 30:18, 27:29',
            'date': '11-06-14',
            'timestamp': 1402448400,
            'time': '04:00',
            'datetime': '11 Jun 2014 04:00'
        }
    """
    try:
        match = {}
        t_data = tr.contents

        """   date & time   """
        try:
            #  table-time datet t1397689200-1-1-0-0
            data = int(t_data[0].get('class')[2].split('-')[0][1:])
            if not data > 1072915201:
                log_rows.error('UTS: %s is older than Jan 2004', data)
            #  2014-06-16 03:00:00
            temp = datetime.datetime.fromtimestamp(data)
            match['timestamp'] = data
            match['datetime'] = temp.strftime("%d %b %Y %H:%M")
            match['date'] = temp.strftime("%d-%m-%y")
            match['time'] = temp.strftime("%H:%M")
        except Exception:
            log_rows.exception('bs4.tag => date & time')

        """ teams """
        try:
            teams = str(t_data[1].find('a').text).split(' - ')
            if not len(teams) == 2 and len(teams[0]) > 3 and len(teams[0]) > 3:
                log_rows.error("Teams is %s", teams)
            match['teams'] = teams
        except Exception:
            log_rows.exception('bs4.tag => teams')

        """ link """
        try:
            match['link'] = str(t_data[1].find('a').get('href'))
        except Exception:
            log_rows.exception('bs4.tag => link')

        """
        get data from sigle match page
        """
        url2 = link[0] + match['link']
        p = requests.get(url2)
        p.encoding = 'ISO-8859-1'
        # second 'soup' is 'borshch'
        borshch = BeautifulSoup(p.content.replace('&nbsp', ' '))

        """   xhash   """
        try:
            text = str(borshch)
            frst = text.find('xhash') + 8
            last = text.find('xhashf') - 3
            xhash = text[frst:last]
            if not len(xhash) == 5:
                log_rows.error('page => xhash is %s', xhash)
                return AssertionError('ASSERT: xhash is ', xhash)
            match['xhash'] = xhash
        except Exception:
            log_rows.exception('page => xhash')

        '''
        <div id="event-status">
            <p class="result:
            ">
               [0]  <span class="bold">Final result </span>
               [1]  <strong>109:108&nbsp;OT&nbsp;(99:99)</strong>
               [2]   (27:25, 17:25, 21:25, 30:20, 8:5)
            </p>
        </div>
        <div id="event-status">
            <p class="result-alert">
                <span class="bold">Canceled</span>
            </p>
        </div>
        '''

        """ score """
        try:
            status = borshch.find(id='event-status')
            temp = status.find('p').get('class')[0] 
            if temp == 'result':               
                match['score'] = [int(x) for x in str(status.strong.text).split(' ')[0].split(':')]
                match['res_box'] = str(status.p.contents[2]).replace('(', '').replace(')', '').lstrip()
                match['ot'] = False if len(match['res_box'].split(', ')) == 4 else True
            elif temp == 'result-alert':
                log_rows.error('Result Alert (match was canseled)')
                return None
            else:
                log_rows.error('Strange page.score error')
                return None
        except Exception:
            log_rows.exception('page => score')

        return match
    except Exception:
        log_rows('Smth wrong with rows_func')


if __name__ == '__main__':
    #  return (asdf, url)
    html = table('2013-2014', 4)
    for i, h in enumerate(html):
        print i + 1, h[0], h[1], rows(h[2])
    """
        {
            'res_box': '34:28, 34:32, 30:29, 27:25',
            'ot': False,
            'timestamp': 1397084400,
            'teams': ['Toronto Raptors', 'Philadelphia 76ers'],
            'score': [125, 114],
            'link': '/basketball/usa/nba-2013-2014/toronto-raptors-philadelphia-76ers-2XbuCZBt/',
            'time': '02:00',
            'date': '10-04-14',
            'datetime': '10 Apr 2014 02:00',
            'xhash': 'yjf41'
        }
    """