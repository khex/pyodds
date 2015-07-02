#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserDict


class Match(UserDict):
    """docstring for ClassName"""

    def __init__(self, slov):
        self.data = {}
        self.update(slov)

    def toster(self):
        return self.__tost

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    __tost = "Za Imeninnika!"

m = Match(dict(first='uno', asdf='eee'))

print(m.toster())
