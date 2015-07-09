from itertools import groupby
from pymongo import MongoClient

teams = (
    'Atlanta', 'Boston', 'Brooklyn', 'Charlotte', 'Chicago',
    'Cleveland', 'Dallas', 'Denver', 'Detroit', 'Golden State',
    'Houston', 'Indiana', 'LA Clippers', 'LA Lakers', 'Memphis',
    'Miami', 'Milwaukee', 'Minnesota', 'New Orleans', 'New York',
    'Oklahoma', 'Orlando', 'Philadel', 'Phoenix', 'Portland',
    'Sacramento', 'San Antonio', 'Toronto', 'Utah', 'Washington')

client = MongoClient("mongodb://localhost:27017/")
db = client["odds_test"]

# res = db.matches.find_one({"xeid": xeid})
# res = db.matches.find({"away.short": "Dallas"}).sort("datetime.timestamp")
# res = db.matches.find({ $or: [ {'home.short': 'Dallas'}, {'away.short': 'Dallas'}]}


def grouper(arg):
    arr = [(k, list(t)) for k, t in groupby(arg, lambda x: x > 0)]
    return arr[0][1]
    # return [len(a[1]) if a[0] is True else -len(a[1]) for a in arr]

for t in teams:
    line, hcap, totl, itot = [], [], [], []
    print('\n', t)
    res = db.matches.find({'$or': [{'home.short': t}, {'away.short': t}]}).sort("datetime.timestamp", -1)

    for r in res:
        if r["season"] == "2014-2015" and r["type"] == "season":
            """   get delta   """
            delta = r["home"]["delta"] if r["home"]["full"] == teams[1] else r["away"]["delta"]

            # набивает массивы по одному числу
            line.append(delta[0])
            hcap.append(delta[1])
            totl.append(delta[2])
            itot.append(delta[3])
    print('line: {}'.format(grouper(line)))
    print('hcap: {}'.format(grouper(hcap)))
    print('totl: {}'.format(grouper(totl)))
    print('itot: {}'.format(grouper(itot)))

"""
for t in teams:
    print '\n', t
    res = db \
        .matches.find({'$or': [{'home.short': t}, {'away.short': t}]}) \
        .sort("datetime.timestamp", -1)
    ind = 1
    for r in res:
        if r["season"] == "2014-2015" and r["type"] == "season":
            line = r["home"]["delta"] \
                if r["home"]["full"] == teams[1] \
              else r["away"]["delta"]
            print "%s %s %s - %s" % (
                #ind,
                r["datetime"]["date"],
                line, r["home"]["full"],
                r["away"]["full"]
            )
            ind += 1
"""
