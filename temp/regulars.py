import re

baskover = 'Final result 128:115 OT (115:115) (27:25, 17:25, 21:25, 30:20, 13:0)'
basknorm = 'Final result 128:115 (45:22, 24:37, 30:25, 9:31)'

baseover = 'Final result 4:3 (0:1, 0:0, 0:0, 0:0, 0:0, 2:0, 0:0, 0:0, 0:1, 2:1)'
basenorm = 'Final result 2:4 (0:0, 0:0, 0:0, 0:3, 0:0, 0:0, 1:1, 0:0, 1:0)'

"""
bask = "Final result 90:100 OT (83:83) (19:21, 19:23, 22:10, 23:29, 7:17)"
base = "Final result 5:3 (0:0, 0:0, 0:0, 0:0, 0:0, 0:0, 1:1, 4:0, X:2)"

bask_full = re.findall('\s+(\d+:\d+)\s+', bask)[0]
bask_main = re.findall('\(([\d+:\d+,*\s*]+)\)', bask)

base_full = re.findall('\s+(\d+:\d+)\s+', bask)[0]
base_main = re.findall('\(([X:\d+,*\s*]+)\)', bask)

print(base_full, base_main)
"""


def quaters(text, sport):
    """ la-la-la """
    match = {}
    if sport == 'basketball':
        if re.search('OT', text):
            match['ot'] = True
            match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
            # ['115:115', '27:25, 17:25, 21:25, 30:20, 13:0']
            re_find = re.findall('\(([\d+:\d+,*\s*]+)\)', text)
            match['main'] = re_find[0]   # '115:115'
            match['quat'] = re_find[1:]  # ['27:25, 17:25, 21:25, 30:20, 13:0']
        else:
            match['ot'] = False
            match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
            match['quat'] = re.findall('\((.+)\)', text)
    elif sport == 'baseball':
        match['full'] = re.findall('\s+(\d+:\d+)\s+', text)[0]
        match['quat'] = re.findall('\(([\d+:\d+,*\s*]+)\)', text)[0]
        match['ot'] = False if len(match['quat'].split(', ')) == 9 else True
    return match

print(quaters(basknorm, 'basketball'))
print(quaters(baskover, 'basketball'))

print(quaters(basenorm, 'baseball'))
print(quaters(baseover, 'baseball'))
