from logger import log_db
from pymongo import MongoClient

#  from pymongo import Connection
#  import pymongo
#  import bson

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
#
#  def db_avaliable():
#    return True

def get_xeid(xeid):
    try:
        temp = db.matches.find_one({'xeid': xeid})
        #  that return None if Exception
        return True if temp is not None else False
    except Exception:
        log_db.exception('Can not get xeid from db')


def save_to_db(match):
    try:
        db.matches.save(match)
        xeid = match['xeid']
        return db.matches.find_one({'xeid': xeid})
    except Exception:
        log_db.exception('Can not save to db')