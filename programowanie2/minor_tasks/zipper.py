#!/usr/bin/env python

# List 2, Task 3, Prog.-L, PWr
# Mateusz Machaj, 20.03.2021

import zipfile
import datetime
import argparse
import os


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str, help = "Path of a directory to archivise.")
args = parser.parse_args()

def zipper(direc:str):
    """
    Function creates a zip for a given directory
    :param directory: path of a drirectory (str)
    Void funct.
    """
    if not os.path.isdir(direc):        
        raise IOError("Path on input not proper.")
    
    # directory to work in
    new_dir = direc + "/../"
    # name of the zip file with a prefix determining a date and time
    zf_name = str(datetime.datetime.today().strftime("%y-%m-%d_%H-%M")) + "_" + os.path.basename(os.path.normpath(direc)) 

    os.chdir(new_dir)
    zf = zipfile.ZipFile(zf_name+".zip", 'w', zipfile.ZIP_DEFLATED)  
    
    for dirname, subdirs, files in os.walk(direc):
        relat_path = os.path.relpath(dirname, new_dir) # relative path to avoid root dirs in structure
        zf.write(relat_path) # first dirs and then in loop files in them

        for filename in files:
            zf.write(os.path.join(relat_path, filename))
                
    zf.close()

zipper(args.directory)
print("Directory archived successfully. Zip saved next to the given directory.")