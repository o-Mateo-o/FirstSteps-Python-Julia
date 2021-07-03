#!/usr/bin/env python

# List 4, Task 2, Prog.-L, PWr
# Mateusz Machaj, 17.04.2021


# NOTE: I didn't use stderr :
# printing messages and handling errors make the program more convenient to use in cmd

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import imageio
import argparse
import random
import shutil
import os
import matplotlib.pyplot as plt

DESKTOP = r"C:\\Users\\cp\\Onedrive\\pulpit"

if __name__ == "__main__":

    # parse all arguments
    parser = argparse.ArgumentParser(
        description='Random walk on a torus. Visualisation mapped to square grid.')
    parser.add_argument('-n', type=int, help="Grid dimension.")
    parser.add_argument('-t', type=int, help="Process duration.")
    parser.add_argument('-i', type=int, nargs=2, help="Initial coordinates - x y.")
    parser.add_argument('-f', type=int, help="Frames per second.")
    args = parser.parse_args()

    def validtest():
        '''
        Test the validity of the given input. 
        *Types are already investigeted by argparse
        :return: In case of issue - False (Bool)
        '''
        argdict = vars(args).copy()
        noneflag = False
        arglist = []
        # presence of arguments
        for aname in argdict.keys():
            if argdict[aname] in [None, []]:
                noneflag = True
                arglist.append(aname)
        if noneflag:
            print(
                "Error: necessary arguments missing on input: {}. ".format(", ".join(arglist))
                    +"Use -h for help.")
            return False
        # positive dimensions
        if args.n < 1:
            print("Error: expected positive size on input.")
            return False
        # initial indices must refer to a point on the created board
        for number in [0,1]: 
            if args.i[number] > args.n or args.i[number] < 1:
                print("Error: initial indices out of a given range.")
                return False
        return True


    def walking(arr, size, initp, time, fps_val):
        '''
        Generate animated gif of random walk.
        :param size: size of a board (int)
        :param initp: initial agent coordinates (tuple of two ints) 
        :param time: number of steps (frames) to generate (int)
        :param fps_val: number of frames per second for animation (int)
        Generates the files, return 0 if fails.
        '''
        fig, ax = plt.subplots(figsize=(7, 5))
        sb.color_palette("cubehelix")
        filenames = []

        dcrt = dircreate()
        if dcrt == 0:
            return 0

        curr_point = initp
        for moment in range(0, time):
            # random movement
            chc = random.choice([[-1, 0], [1, 0], [0, -1], [0, 1]])
            curr_point = ((curr_point[0]+chc[0]) % size,
                          (curr_point[1]+chc[1]) % size)
            arr[curr_point[0],curr_point[1]] += 1
            # plotting
            heat_map = sb.heatmap(arr, xticklabels=False, yticklabels=False,
                                  annot=True, cbar=False,  vmin=0, vmax=12, cmap="Spectral")
            ax.set_aspect('equal')
            ax.set_title('Random walk on a torus.')

            fname = tmppath+"\\{n}.jpg".format(n=moment)

            plt.savefig(fname)
            plt.cla()
            filenames.append(fname)

        gifmake(filenames, fps_val)
        clsw = closeoper()
        if clsw == 0:
            return 0

        print("Animation generated successfully - saved in pulpit/randomwalk.")

    def gifmake(filenames_lst, frames_p_sec_c):
        '''
        Create a gif.
        :param filenames_lst: names of jpg files in temp directory (list)
        :param frames_p_sec_c: fps value (int)
        Void function.
        '''
        with imageio.get_writer(dirpath+"\\anim.gif", mode='I', fps=frames_p_sec_c) as writer:
            for filename in filenames_lst:
                image = imageio.imread(filename)
                writer.append_data(image)

    def closeoper():
        '''
        Delete a temp directory.
        Void function. Returns 0 if fails (if file exists).
        '''
        try:
            shutil.rmtree(tmppath)
        except OSError:
            print("Error: {pth} doesn't exist in the created directory.".format(
                pth=tmppath))
            return 0

    dirpath = "randomwalk"
    tmppath = dirpath+"\\tmp"

    def dircreate():
        '''
        Creates a path for a directory to save contnent in.
        Void function. Returns 0 if fails (if file exists).
        '''
        os.chdir(DESKTOP)  # DESKTOP path
        try:
            os.mkdir(dirpath)
        except OSError:
            print("Error: {pth} already exists on the desktop.".format(
                pth=dirpath))
            return 0
        os.mkdir(tmppath)


    if validtest():
        board = np.zeros((args.n, args.n))
        walking(board, args.n, args.i, args.t, args.f)