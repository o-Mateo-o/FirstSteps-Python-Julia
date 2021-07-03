#!/usr/bin/env python

# List 3, Task 2, Prog.-L, PWr
# Mateusz Machaj, 06.04.2021

import argparse
import os
import string

# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('archive', type=str,
                    help="Name of the archive to unpack in it's root folder.")
args = parser.parse_args()


def unpack(arch_name: str):
    """
    Unpack files from an "archive file" to a directory.
    :param arch_name: path to the archive (str)
    Void funct.
    """

    # dir and file name check
    unp_dir = arch_name+"/../unpacked_" + \
        os.path.basename(arch_name)+"/"  # dir to unpack in
    if not os.path.isfile(arch_name):
        raise IOError("Path on input not proper.")
    if os.path.isdir(unp_dir):
        raise IOError(
            "Cannot unpack to the directory unpacked_[arch name]. It already exist in the root directory.")

    # interpreting line by line
    with open(arch_name, "r") as arch:
        # first loop flags
        loopI = False
        loopE = False
        names_list = []

        try:
            while 1:
                line = arch.readline()
                # firstline is expected to be filename
                if not loopE and line[0] == ':':
                    raise Exception("File type error. Cannot be decoded.")

                # break at the end of the file
                if not line:
                    fil.close()
                    break

                # only filename and ":"-starting lines allowed in our filetype
                if line[0] in list(string.whitespace)+['"', '?', '*', '>', '<', '|']:
                    if loopE:
                        fil.close()
                    raise Exception(
                        "File type error. Cannot be fully decoded.")

                # create directory to unpack in
                if not loopE:
                    os.mkdir(unp_dir)

                # creating a file to write in
                if line[0] != ":":
                    suffix = ""  # along with names_list register adds a number in filename if it repeats
                    if loopI:
                        fil.close()
                    base_name = os.path.basename(line)
                    if base_name in names_list:
                        suffix = "_"+str(names_list.count(base_name))

                    fil = open(
                        unp_dir+base_name[:-5]+suffix+base_name[-5:-1], "w")
                    names_list.append(base_name)

                    loopI = True

                # text conversion
                else:
                    fil.write(line[1:])
                loopE = True
        except:
            raise Exception("Wrong type of the file. Cannot be decoded.")


unpack(args.archive)
print("Unpacked files available in the root directory of te archive.")
