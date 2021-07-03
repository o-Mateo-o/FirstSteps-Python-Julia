#!/usr/bin/env python

# List 4, Task 1, Prog.-L, PWr
# Mateusz Machaj, 17.04.2021


# NOTE: I didn't use stderr :
# printing messages and handling errors make the program more convenient to use in cmd

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os
import imageio
import shutil
import argparse

DESKTOP = r"C:\\Users\\cp\\Onedrive\\pulpit"

if __name__ == "__main__":

    # parse all arguments
    parser = argparse.ArgumentParser(
        description='Oscillation symulations generator.')
    parser.add_argument('-Q', type=float, help="Damping factor - Q.")
    parser.add_argument('-wh', type=float,
                        help="Forcing vib radial velocity factor - omega^.")
    parser.add_argument('-A', type=float, help="Forcing vib amplitude.")
    parser.add_argument('-wi', type=float, help="Initial radial velocity.")
    parser.add_argument('-thi', type=float, help="Initial angle.")
    parser.add_argument('-t', type=float, help="Simulation time in sec.")
    parser.add_argument('-l', type=float, help="Rope length (if animating).")
    parser.add_argument('-p', type=float, help="Precision - difference in time between points.")
    parser.add_argument('--mode', '-m', nargs="*", type=str, default=[], help="Working mode\
                        (angle -ang, velocity - vel, animation - anim).")
    args = parser.parse_args()

    def validtest():
        '''
        Test the validity of the given input. 
        *Types are already investigeted by argparse
        :return: In case of issue - False (Bool)
        '''
        # presence of arguments
        argdict = vars(args).copy()
        del argdict['l']
        noneflag = False
        arglist = []
        # l not needed if no anim mode mentioned
        for aname in argdict.keys():
            if argdict[aname] in [None, []]:
                noneflag = True
                arglist.append(aname)
        if noneflag:
            print(
                "Error: necessary arguments missing on input: {}. ".format(", ".join(arglist))
                  +"Use -h for help.")
            return False
        # if anim given - l is demanded
        if 'anim' in args.mode and args.l == None:
            print("Error: necessary argument -l missing on input. Use -h for help.")
            return False
        # only predefined modes accepted
        for aname in args.mode:
            if aname not in ['anim', 'vel', 'ang']:
                print("Unknown mode: {} ".format(aname))
                return False
        return True

    def pendul(y, tau, Q, A_hat, omg_hat):
        '''
        Function for differential equation given in task.
        :param y: [angle, radial velocity] in/d (list of floats)
        :param tau: time (float)
        :param Q: damping factor (float)
        :param A_hat: forcing vib amplitude (float)
        :param omg_hat: forcing vib radial velocity factor (float)
        :return: [diff of angle, diff of radial velocity] (list of floats)
        '''
        # where Q is responsible for damping magnitude
        # A_hat stands for forcing oscillation amplitude
        # omg_hat can be represented as a ratio of initial pendulum peroid to forcing oscillation peroid
        th, omg = y[0], y[1]
        dth = omg
        # formula from the task (for omega diff)
        domg = (-np.sin(th)-1/Q*omg+A_hat*np.cos(omg_hat*tau+np.pi))
        return [dth, domg]

    def oscillation(function, time, time_delta, initv, Q, A_h, omg_h):
        '''
        Function for differential equation given in task.
        :param function: function to solve (function)
        :param time: time ending time(float)
        :param time_delta: precision of time - step (float)
        :param initv: [initial angle, initial radial velocity] (list of floats)
        :param Q: damping factor (float)
        :param A_hat: forcing vib amplitude (float)
        :param omg_hat: forcing vib radial velocity factor (float)
        :return: (linrange of time, angles in time, velocity in time) (tuple of 3 lists of floats)
        '''
        tau_lst = np.linspace(0, time, int(time/time_delta))
        solut = odeint(function, initv, tau_lst, args=(Q, A_h, omg_h))
        return (tau_lst, solut[:, 0], solut[:, 1])

    # formula of the equation from task and title of plots
    formula = r"$\frac{d^2\theta}{d\tau^2}+\frac{1}{Q}\frac{d\theta}{d\tau}+sin\theta = \hat{A} cos(\hat{\omega}\tau)$"
    title = "Damped-forced vibrations:  " + formula

    def plot_angletime(oscdata):
        '''
        Plot the graph of angles depending on time.
        :param oscdata: data from oscillation function (tuple of 3 lists) - time, angles, velocities
        Void function.
        '''
        plt.figure("Oscillation - angle in time")
        plt.title(title)
        plt.xlabel(r"time - $\tau$")
        plt.ylabel(r"angle - $\theta$")
        plt.plot(oscdata[0], oscdata[1], color="blue")
        print("Plot generated successfully in pyplot window.")

    def plot_rveloctime(oscdata):
        '''
        Plot the graph of velocity depending on time.
        :param oscdata: data from oscillation function (tuple of 3 lists) - time, angles, velocities
        Void function.
        '''
        plt.figure("Oscillation - radial velocity in time")
        plt.title(title)
        plt.xlabel(r"time - $\tau$")
        plt.ylabel(r"radial velocity - $\omega$")
        plt.plot(oscdata[0], oscdata[2], color="orange")
        print("Plot generated successfully in pyplot window.")

    def movement(oscdata, length, prec):
        '''
        Generate animated gif of a pendulum.
        :param oscdata: data from oscillation function (tuple of 3 lists) - time, angles, velocities
        :param length: length of the rope (float)
        :param prec: precision of the time (delta) (float)
        Generates the files, return 0 if fails.
        '''
        fig, ax = plt.subplots(figsize=(5, 5))
        filenames = []

        dcrt = dircreate()
        if dcrt == 0:
            return 0

        stp, frames_p_sec = framesopt(prec)

        for moment in range(0, len(oscdata[0]), stp):
            ax.set_title(title)
            ax.set_xlabel(r"coordinates - $x$")
            ax.set_ylabel(r"coordinates - $y$")
            # to polar coordinates but rotated by -90 degrees
            x = length * np.sin(osc[1][moment])
            y = - length * np.cos(osc[1][moment])
            ax.set_aspect(1)
            plt.ylim((-length-0.4, 0.2))
            plt.xlim((-length-0.2, length+0.2))

            ax.plot([0, x], [0, y], color="black", lw=1,
                    ls='-', marker='o', markersize=10)

            fname = tmppath+"\\{n}.jpg".format(n=moment)
            plt.savefig(fname)
            plt.cla()
            filenames.append(fname)

        gifmake(filenames, frames_p_sec)
        clsw = closeoper()
        if clsw == 0:
            return 0

        print("Animation generated successfully - saved in pulpit/oscmovement.")

    dirpath = "oscmovement"
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

    def framesopt(precf):
        '''
        Return an optimal solution for efficien gif fps.
        :param precf: time precision(delta) (float)
        :return: (step in time, fps value) (tuple of ints)
        '''
        stpf = 1
        p_sec = 1/precf
        frames_p_secf = 1
        # if too dense, ommit unneeded frames while rendering
        if p_sec >= 30:
            frames_p_secf = 30
            stpf = int(p_sec/30)
        else:
            frames_p_secf = p_sec
        return (stpf, frames_p_secf)

    if validtest():
        # if no errors assign the variables from input
        damp_fct = args.Q
        forc_vel_fct = args.wh
        forc_ampl = args.A
        th0 = args.thi
        omg0 = args.wi
        initvals = [th0, omg0]
        rp_length = args.l

        duration_time = args.t
        time_precis = args.p
        modes = args.mode

        # generate the solution of an equation
        osc = oscillation(pendul, duration_time, time_precis,
                          initvals, damp_fct, forc_ampl, forc_vel_fct)

        # for each mode mentioned do a proper action
        showflag = False
        if 'vel' in modes:
            plot_rveloctime(osc)
            showflag = True
        if 'ang' in modes:
            plot_angletime(osc)
            showflag = True
        if showflag:
            plt.show()
        if 'anim' in modes:
            movement(osc, rp_length, time_precis)
