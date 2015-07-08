from pymongo import MongoClient

teams = (
    'Atlanta', 'Boston', 'Brooklyn', 'Charlotte', 'Chicago',
    'Cleveland', 'Dallas', 'Denver', 'Detroit', 'Golden State',
    'Houston', 'Indiana', 'LA Clippers', 'LA Lakers', 'Memphis',
    'Miami', 'Milwaukee', 'Minnesota', 'New Orleans', 'New York',
    'Oklahoma', 'Orlando', 'Philadel', 'Phoenix', 'Portland',
    'Gopas',
    'Sacramento', 'San Antonio', 'Toronto', 'Utah', 'Washington')

client = MongoClient("mongodb://localhost:27017/")
db = client["odds_test"]

# res = db.matches.find_one({"xeid": xeid})
# res = db.matches.find({"away.short": "Dallas"}).sort("datetime.timestamp")
# res = db.matches.find({ $or: [ {'home.short': 'Dallas'}, {'away.short': 'Dallas'}]}

t = 'Charlotte'
print('\n', t)
res = db \
    .matches.find({'$or': [{'home.short': t}, {'away.short': t}]}) \
    .sort("datetime.timestamp", -1)
ind = 1
for r in res:
    if r["season"] == "2014-2015" and r["type"] == "season":
        delta = r["home"]["delta"] if r["home"]["full"] == teams[1] else r["away"]["delta"]
        print("{} {} {} {} - {}".format(
              ind,
              r["datetime"]["date"],
              delta,
              r["home"]["full"],
              r["away"]["full"]))
        ind += 1
