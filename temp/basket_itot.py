#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def itot_basket(total, h_cap):
    """
    Returns:
        a value of individual handyCap like:
        92.5 or 101.5
    """
    abs_cup = abs(h_cap)
    half_totl = (total - abs_cup) / 2  # 95.0 or 95.5
    hand_even = (abs_cup - 0.5) % 2 == 0
    # тотал > чет
    if (total - 0.5) % 2 == 0:
        # фора > чет
        if hand_even:
            return half_totl + abs_cup if h_cap < 0 else half_totl + 0.5
        # фора > нечет
        else:
            return half_totl + abs_cup + 0.5 if h_cap < 0 else half_totl
    # тотал > нечет
    else:
        # фора > чет
        if hand_even:
            return half_totl + abs_cup + 0.5 if h_cap < 0 else half_totl
        # фора > нечет
        else:
            return half_totl + abs_cup if h_cap < 0 else half_totl + 0.5


if __name__ == '__main__':

    print(itot_basket(208.5, -4.5), itot_basket(208.5, 4.5))
    print(itot_basket(196.5, -5.5), itot_basket(196.5, 5.5))
    print(itot_basket(205.5, -4.5), itot_basket(205.5, 4.5))
    print(itot_basket(205.5, -3.5), itot_basket(205.5, 3.5))

    print(itot_basket(195.5, -3.5), itot_basket(195.5, 3.5))
