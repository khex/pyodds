#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from logger import log_db
"""
import pymongo, bson
from pymongo import Connection
"""

client = MongoClient('mongodb://localhost:27017/')
db = client['deltabase']
# teams = db['teams'] == db.teams
# matches = db['matches'] == db.matches

#  db.drop_collection('matches')
#  def db_avaliable(): return True


def get_xeid(xeid):
    try:
        temp = db.matches.find_one({'xeid': xeid})
        # that return None if Exception
        return True if temp is not None else False
    except Exception:
        log_db.exception('Can\'t get \'xeid\' from DataBase')

"""
def team_insert(argy):
    # in v3.02 use insert_one() or insert_many()
    try:
        if type(argy) is list or type(argy) is tuple:
            result = db.test.insert_many(argy)
        elif type(argy) is dict:
            result = db.test.insert_many(argy)
        else:
            raise('Can\'t save becouse argy is not a tuple, list or dict')
        return result
    except Exception as e:
        raise(e)


def foos():
    как достать все команд NBA етого сезона:
        1. все команд с tid от 1 - 30
        2. cursor -> baseball, usa, nba, 2015
    return specific fields:
        - full and short
    pass


def save_to_db(match):
    try:
        db.matches.save(match)
        xeid = match['xeid']
        return db.matches.find_one({'xeid': xeid})
    except Exception:
        log_db.exception('Can not save to db')


def team_insert(argy):
    # in v3.02 use insert_one() or insert_many()
    print(type(argy))
    try:
        if type(argy) is list or type(argy) is tuple:
            print('List or Tuple')
            result = db.teams.insert_many(argy)
        elif type(argy) is dict:
            print('Is Dict')
            result = db.teams.insert_many(argy)
        else:
            raise('Can\'t save becouse argy is not a tuple, list or dict')
        return result
    except Exception as e:
        raise(e)
"""
