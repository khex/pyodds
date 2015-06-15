#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
bin\mongod.exe --config mongodb.conf
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


class Module(object):
    """
    self.__modules заменяет 'db.modules.insert_one()'
    """

    def __init__(self):
        self.__modules = db['modules']

    def save(self, arg):
        return self.__modules.insert_one(arg).inserted_id

    """
    def get_id(self, mid):
        try:
            return self.__modules.find_one({'mid': mid})['_id']
        except Exception as e:
            raise(e)
    """


class Team(object):
    """
    self.__teams заменяет 'db.teams.insert_many()'
    """

    def __init__(self):
        self.__teams = db['teams']

    def save(self, teams, m_id):
        for t in teams:
            t['module'] = ObjectId(m_id)
        return self.__teams.insert_many(teams).inserted_ids

    """
    def read(self, mid):
        return self.__modules.find_one({'mid': mid})
    """

module = Module()
team = Team()
