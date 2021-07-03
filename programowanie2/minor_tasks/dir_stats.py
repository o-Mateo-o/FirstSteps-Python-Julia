#!/usr/bin/env python

# List 2, Task 4, Prog.-L, PWr
# Mateusz Machaj, 20.03.2021

import argparse
import os
import time


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str,
                    help="Path of a directory show annual stats.")
args = parser.parse_args()


def stats(direc: str):
    """
    Function gives a yearly statistics of file modification
    :param directory: path of a drirectory (str)
    Void funct saves a result in file od desktop.
    """
    if not os.path.isdir(direc):
        raise IOError("Path on input not proper.")

    # desktop
    DSK = "C:/Users/cp/OneDrive/pulpit"
    file_reg = []

    for dirname, subdirs, files in os.walk(direc):
        for filename in files:
            # list of tuples ('year of mod.', 'filename') for all the files in given dir
            file_reg.append((time.strftime('%Y', time.gmtime(
                os.path.getmtime(os.path.join(dirname, filename)))), filename))

    # time boundaries and a dictionary with lists of files for a given year; then fillig it up
    def get_yr(el): return int(el[0])
    min_year = min([get_yr(el) for el in file_reg])
    max_year = int(time.strftime('%Y', time.gmtime(time.time())))
    report = {year: [] for year in range(min_year, max_year+1)}

    for tup in file_reg:
        report[get_yr(tup)].append(tup[1])

    # sorted list of years
    keys_list = list(report.keys())
    keys_list.sort(reverse=True)

    files_total = len(file_reg)
    # another dictionary, where each year-key has got assigned a number of modified files
    files_years = {year: len(report[year]) for year in keys_list}


    # writing it all into the stats_time file on the desktop
    with open(DSK+"/stats{tm}.txt".format(tm=str(time.time())[:10]), 'w') as fl:
        # numeric stats
        fl.write("Annual file modification statistics for {dirname}\n###################################\n\n"
                 .format(dirname=direc))
        for key in keys_list:
            fl.write("Files modified in {year}: {number}/{total}\n".format(
                year=key, number=files_years[key], total=files_total))
        fl.write("\n\n")
        # file lists for each year
        for key in keys_list:
            fl.write("List of files modified in {year}:\n-----------------\n".format(
                year=key))
            for filename in report[key]:
                fl.write(filename+", ")
            fl.write("\n\n")


stats(args.directory)
print("Stats file generated on desktop.")
