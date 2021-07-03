#!/usr/bin/env python

# List 3, Task 4, Prog.-L, PWr
# Mateusz Machaj, 06.04.2021

import re
import codecs
import os
import argparse

# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('--system', '-s', type=str, default='win', help="Target system (win or unix).")
parser.add_argument('files', type=str, nargs="*", help="Files to convert. Absolute paths expected.")
args = parser.parse_args()


def newlineconv(system:str, file_names: list):
    """
    Convert new line char between unix and win OS.
    :param system: name of the system - win or unix (str)
    :param files: list of text files to convert (list of str)
    Void funct.
    """

    DSK = "C:/Users/cp/OneDrive/Pulpit/"

    # Presence and extension test for each text file
    for name in file_names:
        if not os.path.isfile(str(name)):
            raise OSError("Paths of files on input not proper.")
        if name[-4:] != ".txt":
            raise OSError("File types on input not proper. '.txt' expected.")
    
    # system name argument
    if system not in ['win', 'unix']:
        raise Exception("Invalid system name.")

    # dir to save in and unless it exists, create one
    new_dir = DSK+"converted_"+system+"/"  
    if os.path.isdir(new_dir):
        raise OSError("Directory with converted files already exists.")
    os.mkdir(new_dir)


    names_list = [] #as below

    for name in file_names:
        suffix = ""  # along with names_list register adds a number in filename if it repeats
        # to avoid overwriting one file
        base_name = os.path.basename(name)
        if base_name in names_list:
            suffix = "_"+str(names_list.count(base_name))

        # open two files binary and copy converted data
        with open(name, 'rb') as source:
            with open(new_dir+base_name[:-4]+suffix+base_name[-4:], 'wb') as prod:
                try:
                    while 1:
                        line = source.readline()
                        if not line: break
                        # new line chr substitution
                        if system == 'unix':
                            prod.write(re.sub(b"(\r\n)",b"\n", line))
                        else:
                            prod.write(re.sub(b"\n",b"\r\n", line))
                except:
                    raise Exception("Wrong type of the file. Cannot be decoded.")
                    
        names_list.append(base_name)

newlineconv(args.system, args.files)
print("Files converted successfully. Saved on desktop.")