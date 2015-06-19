#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# $ py.test -v test_tabler.py

import sys
import pytest

# http://stackoverflow.com/questions/714063/
sys.path.append('C:/Users/qm69/Code/delta_odds')

from libs.tabler import get_table


@pytest.fixture(scope="module")
def bc():  # ball_counter == bc
    return get_table('draw_list', 5053)


class TestClass:

    def test_tabler(self, bc):

        # test the whole list
        assert type(bc) is list
        assert len(bc) == 80

        # test each ball from list
        for ball in bc:
            assert type(ball) is dict
            assert len(ball) == 8

            # ball
            assert type(ball['ball']) is int
            assert ball['ball'] < 81

            # drop
            assert type(ball['drop']) is int
            assert ball['drop'] > 0

            # tabler => rows_to_dict => get date & time
            if not data > 1072915201:
                log_tabler.error('UTS: %s is older than Jan 2004', data)
