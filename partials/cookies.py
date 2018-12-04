#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

cook = {'_ga': 'GA1.2.1893429700.1543740290', '_gid': 'GA1.2.1021029589.1543740290', '_gat_UA-821699-19': 1}
link = 'https://fb.oddsportal.com/ajax-sport-country-tournament-archive/3/C2416Q6r/X0/1/3/1?_=1432400166447'
r = requests.get(link,
	headers={
	  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
	  'referer': 'https://www.oddsportal.com/basketball/usa/nba/philadelphia-76ers-dallas-mavericks-fL8bbADr/'
	},
	# cookies={'_ga': 'GA1.2.1893429700.1543740290', '_gid': 'GA1.2.1021029589.1543740290', '_gat_UA-821699-19': '1'},
)
print(r.text)
"""
:path: /feed/match/1-3-fL8bbADr-1-2-yjf87.dat?_=1543756871915
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7
cache-control: no-cache
cookie: _ga=GA1.2.1893429700.1543740290; _gid=GA1.2.1021029589.1543740290; _gat_UA-821699-19=1
pragma: no-cache
referer: https://www.oddsportal.com/basketball/usa/nba/philadelphia-76ers-dallas-mavericks-fL8bbADr/
user-agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36

accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7
cache-control: no-cache
cookie: _ga=GA1.2.1893429700.1543740290; _gid=GA1.2.1021029589.1543740290
pragma: no-cache
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36
"""