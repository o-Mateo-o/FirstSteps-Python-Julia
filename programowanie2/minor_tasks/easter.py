#!/usr/bin/env python

# List 2, Task 1, Prog.-L, PWr
# Mateusz Machaj, 20.03.2021

import math as mt
import datetime
import argparse


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('year_input', type=int, help = "Year to calculate the date of.")
args = parser.parse_args()

def meeus(year:int) -> datetime.date:
    """
    Function determine the date of Easter in given year.
    :param year: year - greater than 33 which stands for Ressurection (int)
    :return: demanded date of Easter (datetime.date)
    Exceptions:
    ValueError if input type is not integer
    Exception("J...") if year is lesser than 33
    """
    try: 
        year = int(year)
    except:
        raise ValueError("Year should be an integer.")

    if year == 0:
        raise ValueError("No such a year.")
    if year < 33:
        raise Exception("Jesus hasn't risen from the dead yet.")

    # steps of the Meeus algorithm
    a = year % 19
    b = mt.floor(year / 100)
    c = year % 100
    d = mt.floor(b / 4)
    e = b % 4
    f = mt.floor((b + 8) / 25)
    g = mt.floor((b - f + 1) / 3)
    h = (19 * a + b - d - g + 15) % 30
    i = mt.floor(c / 4)
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = mt.floor((a + 11 * h + 22 * l) / 451)
    p = (h + l - 7 * m + 114) % 31

    day = p + 1
    month = mt.floor((h + l - 7 * m + 114) / 31)

    return datetime.date(year = year, day = day, month = month)

print(meeus(args.year_input))