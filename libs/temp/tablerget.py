import datetime
import requests
import json
from bs4 import BeautifulSoup


link = "http://www.oddsportal.com/baseball/usa/mlb/results/"
q = requests.get(link)
if q.status_code != 200:
    print('results page status code is {}'.format(q.status_code))
q.encoding = 'ISO-8859-1'

q_string = str(q.content)

soup = BeautifulSoup(q.content)

print(q_string)
