from delta_odds.logger import log_db
from pymongo import MongoClient
from pymongo import Connection
import pymongo
import bson

"""
sudo rm /var/lib/mongodb/mongod.lock
mongod --dbpath /data/db --repair --repairpath /data/db0
sudo service mongod restart

http://cheat.errtheblog.com/s/mongo
"""


client = MongoClient('mongodb://localhost:27017/')
db = client['odds_test']
#  collection = db['test-collection']
#  db.drop_collection('matches')


def db_avaliable():
    return True


def get_xeid(xeid):
    pass

def save_to_db(match):
    db.matches.save(match)
    print db.matchess.find_one({'xeid': match['xeid']})