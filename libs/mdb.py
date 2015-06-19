#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
bin/mongod.exe --config mongodb.conf
"""

from pymongo import MongoClient
# db.things.find_one({'_id': ObjectId('4ea113d6b684853c8e000001') })
from bson.objectid import ObjectId

# from logger import log_db
# import pymongo, bson

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['delta_test']
except Exception as e:
    raise(e)

#  check if Mongodb is avaliable
#  if not mongo_avaliable():
#    raise Exception('MongoDB is not avaliable!')
#       pymongo.errors.ConnectionFailure


class Module(object):
    """ self.__modules заменяет 'db.modules.insert_one()' """
    def __init__(self):
        self.__modules = db['modules']

    def save_n_back(self, mdl):
        m_id = self.__modules.insert_one(mdl).inserted_id
        return self.__modules.find_one({'_id': m_id})

    # def get_id(self, mid):
    #    return self.__modules.find_one({'mid': mid})['_id']


class Team(object):
    """ self.__teams заменяет 'db.teams.insert_many()' """
    def __init__(self):
        self.__teams = db['teams']

    def save(self, teams):
        return self.__teams.insert_many(teams).inserted_ids

    def find(self, full):
        return self.__teams.find_one({'full': full})


class Match(object):
    """docstring for Match"""
    def __init__(self):
        self.__teams = db['matches']

    def get_xeid(self, xeid):
        return True

modules = Module()
teams = Team()
matches = Match()
