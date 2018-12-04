#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cd 'C:/env/mongodb/'
bin/mongod.exe --config mongodb.conf
"""

from pymongo import MongoClient
# import pymongo, bson
# from bson.objectid import ObjectId
from logger import log_db

""" for local mongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['delta_test']
"""
""" https://mongolab.com
    Account name: qm69    pass: saturn69
    DBUser  name: stavros pass: balalajka7
    Email: qm69@ua.fm
"""

MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()


class Teams(object):
    """docstring for ClassName"""

    def __init__(self):
        self.__teams = db['teams']

    def save_one(self, team):
        return self.__teams.insert_one(team).inserted_id

    def save_many(self, teams):
        return self.__teams.insert_many(teams).inserted_ids

    def find_one(self, full_name):
        return self.__teams.find_one({'full': full_name})


class Matches(object):
    """docstring for ClassName"""
    def __init__(self):
        self.__matches = db['matches']

    def save_one(self, match):
        return self.__matches.insert_one(match).inserted_id

    def find_xeid(self, xeid):
        return self.__matches.find_one({'xeid': xeid})

    def delete_many(self, league):
        return self.__matches.remove({"league": league})


class Modules(object):
    """docstring for ClassName"""
    def __init__(self):
        self.__modules = db['modules']

    def save_one(self, mdl):
        m_id = self.__modules.insert_one(mdl).inserted_id
        # return self.__modules.find_one({'_id': m_id})
        return m_id

teams   = Teams()
matches = Matches()
modules = Modules()
