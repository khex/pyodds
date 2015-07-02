#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cd 'C:\env\mongodb\'
bin/mongod.exe --config mongodb.conf
"""

from pymongo import MongoClient
# import pymongo, bson
# from bson.objectid import ObjectId
# from logger import log_db


class MongoDB(object):
    """docstring for ClassName"""
    def __init__(self, db_name):
        try:
            self.__client = MongoClient('mongodb://localhost:27017/')
            self.__db = self.__client[db_name]
            self.__db.collection_names()
            self.__teams = self.__db['teams']
            self.__matches = self.__db['matches']
            self.__modules = self.__db['modules']
        except Exception as ex:
            print('-= MongoDB ne dostupna=-\n{}'.format(ex))

    """ Team methods """
    def team_save(self, teams):
        return self.__teams.insert_many(teams).inserted_ids

    def team_find(self, full):
        return self.__teams.find_one({'full': full})

    """ Match methods """
    def match_get_xeid(self, xeid):
        return False  # True

    """ Module methods """
    def module_save_n_back(self, mdl):
        m_id = self.__modules.insert_one(mdl).inserted_id
        return self.__modules.find_one({'_id': m_id})

monga = MongoDB('delta_test')
