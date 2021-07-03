#!/usr/bin/env python

# List 3, Task 3, Prog.-L, PWr
# Mateusz Machaj, 06.04.2021

import argparse
import os
from shutil import copyfile
import time


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('--extension', '-e', nargs="*", type=str,
                    default=[], help="Extensions of the files to copy.")
parser.add_argument('--directories', '-d', nargs="*", type=str,
                    default=[], help="Directories to arch. Absolute paths expected.")
args = parser.parse_args()


def bckp(extens: str, direcs_list: str):
    """
    Copy files of given extesions and directories to backup directory.
    :param extens: extensions of files to copy (list of str)
    :param direcs_list: path of drirectories to search in (list of str)
    Void funct saves a result in directory (at cp).
    """

    PERIOD = 3*24*60*60  # Time of 3 days
    # list of tuples ('seconds since modification', 'filename') for all the files
    file_reg = []
    now = time.time()
    now_fmt = time.strftime("%Y-%m-%d", time.gmtime(now))
    new_dir = "C:\\Users\\cp\\Backup\\copy-"+now_fmt  # backup dir

    # validity of extension format
    for exten in extens:
        if exten[0] != ".":
            raise IOError("Not valid extensions.")

    # presence of given paths
    for name in direcs_list:
        if not os.path.isdir(str(name)):
            raise OSError("Paths on input not proper.")

    # in case copy is already done that day
    if os.path.isdir(new_dir):
        raise OSError("Valid backup already exists.")

    # creating ~/Backup/copyXXX
    if not os.path.exists(new_dir+"\\.."):
        os.mkdir(new_dir+"\\..")
    os.mkdir(new_dir)

    # filling up the list of all files in given dirs
    for direc in direcs_list:
        for dirname, subdirs, files in os.walk(direc):
            for filename in files:
                file_reg.append(
                    (now - os.path.getmtime(os.path.join(dirname, filename)), os.path.join(dirname, filename)))

    names_list = []

    for exten in extens:
        for elem in file_reg:
            suffix = ""  # along with names_list register adds a number in filename if it repeats
            # copying file from list to backup dir if it isn't too old and has a right extension
            # if files repeat use suffix
            if elem[0] < PERIOD and elem[1][(-len(exten)):] == exten:
                base_name = os.path.basename(elem[1])
                if base_name in names_list:
                    suffix = "_"+str(names_list.count(base_name))
                copyfile(elem[1], new_dir+"\\"+base_name[:-
                         len(exten)]+suffix+base_name[-len(exten):])
                names_list.append(base_name)


bckp(args.extension, args.directories)
print("Backup generated in home directory at 'Backup'.")
