#!/usr/bin/env python

# List 3, Task 1, Prog.-L, PWr
# Mateusz Machaj, 06.04.2021

import argparse
import os


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('archive', type=str, help = "Name of the generated file (If root not given, arch will be saved on desktop).")
parser.add_argument('files', nargs="*", type=str, help = "Text files to archive. Absolute paths expected.")
args = parser.parse_args()

def archivise(arch_name:str, file_names: list):
    """
    Create a custom "archive file" from given text files.
    :param arch_name: name or path of the archive - if only the name, root will be a desktop (str)
    :param filr_names: list paths to text files (list of str)
    Void funct.
    """
    # desktop
    DSK = "C:/Users/cp/OneDrive/Pulpit/"
    
    # Presence and extension test for each text file
    for name in file_names:
        if not os.path.isfile(str(name)):
            raise OSError("Paths of files on input not proper.")
        if name[-4:] != ".txt":
            raise OSError("File types on input not proper. '.txt' expected.")
    
    # Check if the archive name is already taken
    arch_name = str(arch_name)        
    arch_name_spl = os.path.split(arch_name)
     
    if arch_name_spl[0] != "" and os.path.exists(arch_name):
        raise OSError("File or directory of a given name already exists. Can't generate an archive.")
    elif arch_name_spl[0] == "" and os.path.exists(DSK+arch_name_spl[1]):
        raise OSError("File or directory of a given name already exists on the desktop. Can't generate an archive.")

    # desktop as deafult
    os.chdir(DSK)

    # in order not to overload, read each line of current file and save it separately into the arch
    # archive stores filenames (and paths) and properly marked contents 
    loop = False    # new line flag before files - except the first
    prefix = ""

    with open(arch_name, "w") as arch:
        for fname in file_names:

            if loop == True: prefix = "\n"
            arch.write(prefix+fname+"\n")

            with open(fname, "r") as fil:
                try:
                    while 1:
                        line = fil.readline()
                        if not line: break
                        arch.write(":"+line)
                except:
                    raise Exception("Wrong type of the file. Cannot be decoded.")

            loop = True # each next file should have new line symbol before path
    

archivise(args.archive, args.files)
print("Files archived successfully. (By deafult archive saved on desktop.)")