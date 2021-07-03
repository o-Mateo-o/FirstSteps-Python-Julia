#!/usr/bin/env python

# List 2, Task 2, Prog.-L, PWr
# Mateusz Machaj, 20.03.2021

from PIL import Image
import argparse
import os


# argument parsing allows us to use the program in console
parser = argparse.ArgumentParser()
parser.add_argument('imi', type=str, help = "Path to an image (of type .jpg).")
parser.add_argument('xi', type=int, help = "New width.")
parser.add_argument('yi', type=int, help = "New height. If 0 it will be set using input proportions.")
args = parser.parse_args()

def mini_jpg(image:str, dim_x:int, dim_y:int):
    """
    Function scales given picture (from file) and saves it in another.
    :param image: path to an input image (str)
    :param dim_x: width of the miniature (int)
    :param dim_y: height of the miniature (int)
    Void function creates the file in the same directory with a name "FILE_mini.jpg" 
    """
    # checking for path validity

    if not os.path.isfile(image):        
        raise IOError("Path on input not proper.")
    filename = os.path.basename(image)
    splt = os.path.splitext(filename)
    if splt[1] != ".jpg":   # extension
        raise IOError("Wrong file type.")

    # additional security (as if we use only the function)
    if type(dim_x) != int or type(dim_y) != int:
        raise TypeError("Wrong input type. Integer expected for the dimensions.")

    new_path = os.path.dirname(image) + "/" + splt[0] + "_new" + splt[1]    # creating new file path with suffix

    if os.path.isfile(new_path):
        raise Exception("File of this name already exists!")    # checking if new path is not leading to the existing file

    im = Image.open(image) 
    width, height = im.size

    # in case the second argument is 0 scale it evenly
    if dim_y == 0:
        dim_y = (height * dim_x)//width
    if dim_x <= 0 or dim_y <= 0:
        raise ValueError("Given dimensions not proper.")

    # ... thumbnail should be a thumbnail
    if width-dim_x < 0 or height-dim_y < 0:
        raise ValueError("Too large dimensions.")

    im = im.resize((dim_x,dim_y), Image.ANTIALIAS)
    im.save(new_path)
        

mini_jpg(args.imi, args.xi, args.yi)
print("Thumbnail saved succesfully.")

