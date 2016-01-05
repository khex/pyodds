# %matplotlib inline
from itertools import groupby
from pymongo import MongoClient
import matplotlib.pyplot as plt

MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

# http://docs.mongodb.org/manual/core/read-operations-introduction/
teams = list(db.teams.find({'$and': [{'tid': {'$gte': 0}}, {'tid': {'$lte': 99}}]},
                           {'full': 1, 'short': 1}).sort('full', 1))
full_names = [team['full'] for team in teams]
short_names = [team['short'] for team in teams]


def grouper(arg):
    # k= True or False, t = массив серии
    resp = [list(t)for k, t in groupby(arg, lambda x: x > 0)][0]
    return [float(len(resp)), 'g'] if resp[0] > 0 else [float(len(resp)), 'r']

mega_list = [[[] for i in range(4)] for r in range(3)]  # 4 * 3
game_place = ['Ever', 'Home', 'Away']
odds_type = ['Line', 'handyCap', 'Total', 'iTotal']

for name in full_names:
    match_list = db.matches.find({
        'league': 'nba',
        # 'season': '2015',
        'seas_type': 'season',
        '$or': [{'home.team': name}, {'away.team': name}]}).sort([('date.iso', -1)])

    arry = [[[] for i in range(4)] for r in range(3)]  # 4 * 3
    for match in match_list:

        """   get delta   """
        delta = match["home"]["ftot"]["delta"] if match["home"]["team"] == name else match["away"]["ftot"]["delta"]
        [arry[0][n].append(delta[n]) for n in range(4)]
        [arry[1][n].append(match["home"]["ftot"]["delta"][n]) for n in range(4) if match["home"]["team"] == name]
        [arry[2][n].append(match["away"]["ftot"]["delta"][n]) for n in range(4) if match["away"]["team"] == name]

    # ['Atlanta Braves', [-3.0, 'r']],
    [[mega_list[r][i].append([name, grouper(arry[r][i])]) for i in range(4)] for r in range(3)]

# print(mega_list)

for i in range(4):
    for r in range(3):
        data = [r[1][0] for r in mega_list[r][i]]
        clrs = [r[1][1] for r in mega_list[r][i]]
        print(data, clrs)
        dlina = range(len(data))

        plt.figure(figsize=(15, 5))
        plt.xticks(dlina, short_names, ha='left', rotation='vertical', fontsize=12)
        ax = plt.axes()
        ax.set_title('{}: {}'.format(game_place[r], odds_type[i]))
        bars = ax.bar(dlina, data, color=clrs)

        for rect in bars:
            height = rect.get_height() + 0.1
            length = rect.get_x() + rect.get_width() / 2.
            text = int(rect.get_height())
            ax.text(length, height, text, ha='center', va='bottom')
