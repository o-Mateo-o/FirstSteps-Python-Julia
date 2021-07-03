# ------------------------------------------------------------------------------
#                            List 7, WDIiP-L, PWr
#                          Mateusz Machaj, 16.01.2021
#
#                                     NOTES:
#
#                     - no task 2 because task 3 includes it
#                - class adjustments (task 4) marked with comments:
#                   * name attribute added
#                   * modification in the constructor function
#                   * destructor function added
#                   * travelled distance and info about in when destructing
#                   * function telling what is tha state of a machine -
#                     if it's total distance greater than 100 - considered as Bad (False)
#                     ~the assumption that more travelling make destroys it~
#
# ------------------------------------------------------------------------------

import random
import matplotlib.pyplot as plt


class Rocket:  # names make the class obvious so no unnecessary comments
    path_length = 0  # ADJUSTMENT 4 - distance travelled

    def __init__(self, name: str, coord: tuple = (0, 0)):
        self.coord = coord  # coordinates - (x,y)
        self.name = name  # ADJUSTMENT 1 - parameter (name of the machine)
        print("Rocket {} launched.".format(self.name))  # ADJUSTMENT 2

    def move(self, vector):  # moving a rocket by a vector (x,y) + counting travelled distance
        self.coord = (self.coord[0] + vector[0], self.coord[1] + vector[1])
        self.path_length += (vector[0] ** 2 + vector[1] ** 2) ** 0.5  # ADJUSTMENT 4 - modifying function

    def r_state(self):  # ADJUSTMENT 5 - telling if the state of machine is good
        if self.path_length > 100:
            return False
        else:
            return True

    def get_position(self):  # getting rockets position (x,y)
        return self.coord

    def get_name(self):  # ADJUSTMENT 1 - function (getting machine's name)
        return self.name

    def get_path_length(self):  # ADJUSTMENT 4 - "get" function (travelled distance)
        return self.path_length

    def get_distance(self, rocket2):  # getting distance between two rockets
        return ((self.coord[0] - rocket2.get_position()[0]) ** 2 +
                (self.coord[1] - rocket2.get_position()[1]) ** 2) ** 0.5

    def __del__(self):  # ADJUSTMENT 3, 4+ and 5+
        state = "Good" if self.r_state() else "Bad"  # Word representation for boolean
        print("Rocket {} blasted.".format(self.name),  # Some info
              "Total distance is {:.3f}.".format(self.path_length),
              "State of the machine - {}.".format(state))


def initializing(cls_name, numb: int, fld_range: tuple = (-10, 10, -10, 10)) -> list:
    """
    Create machines and return list of them.
    :param cls_name: a class - for creating rockets should be Rocket
    :param numb: number of discs
    :param fld_range: range of a field (x_min, x_max, y_min, y_max)
    """
    if type(fld_range) != tuple or type(numb) != int:  # security - type checking
        print("Wrong data type")
        return []
    elif len(fld_range) != 4:
        print("Wrong range.")
        return []

    cnt = 0  # counter
    obj_list = []  # list of machines

    try:
        while 1:  # in loop create n rockets with random coordinates and proper name
            r_x = random.uniform(fld_range[0], fld_range[1])
            r_y = random.uniform(fld_range[2], fld_range[3])
            obj_list.append(cls_name("Спутник" + str(cnt + 1), (r_x, r_y)))
            cnt += 1
            if cnt >= numb:
                break
    except:
        print("Initializing the objects is not possible.")
        return []

    return obj_list


def report(objs: list, number: int = 0) -> list:
    """
    Print out current positions and distances. Return a list of positions.
    :param objs: list of rockets
    :param number: number in title of the report
    """
    positions = []  # list of current rockets positions - a tuple of (name, coordinates)
    try:  # if something is wrong with the machines do not continue
        for r in objs:
            positions.append((r.get_name(), r.get_position()))
    except:
        print("Wrong input for a report.")
        return []

    print("######################################################")
    info = "" if number == 0 else "number " + str(number)  # Print a title - with number if given
    print("Rockets position report", info)
    print("------------------------------------------------------")
    print("POSITIONS:\n")

    for r in positions:  # print positions with names
        print(r[0], ": ", r[1])

    print("\nDISTANCES:\n")
    for r1 in objs:  # print distance between every two rockets
        for r2 in objs:
            if objs.index(r2) > objs.index(r1):
                print(r1.get_name(), "-", r2.get_name(), ": ", r1.get_distance(r2))
    print("######################################################")

    return positions


def moving(objs: list, fld_rng: tuple):
    """
    Randomly move rockets from the list within a given field.
    :param objs: list of rockets
    :param fld_rng: range of a field (x_min, x_max, y_min, y_max)
    """
    try:  # if objects are proper move each of them by a random vector within a field range
        for rct in objs:
            vector = (random.uniform(fld_rng[0] - rct.get_position()[0], fld_rng[1] - rct.get_position()[0]),
                      random.uniform(fld_rng[2] - rct.get_position()[1], fld_rng[3] - rct.get_position()[1]))
            rct.move(vector)
    except:
        print("Error. Moving is not possible.")


def void_m(objs: list, mvs_nr: int, fld_rng):
    """
    Print out reports and move rockets times a given number.
    ### Plot the results
    :param objs: list of rockets
    :param mvs_nr: number of expected moves
    :param fld_rng: range of a field (x_min, x_max, y_min, y_max)
    """
    if type(mvs_nr) != int or (type(mvs_nr) == int and mvs_nr < 0):  # check if type of moves number proper
        print("Wrong moves number.")
        return

    positions_list_raw = []  # list where each element is a list of positions in specified moment
    for i in range(1, mvs_nr + 1):  # move rockets for a given number of times printing out a report and moving
        positions_list_raw.append(report(objs, i))  # making a report and additional positions saving
        moving(objs, field_range)
        if i == mvs_nr:  # pre-final report
            positions_list_raw.append(report(objs, i + 1))
    # transpose raw list to the one easier to use
    positions_list = []
    for n in range(0, len(positions_list_raw[0])):
        positions_list.append([])
        for rap in positions_list_raw:
            positions_list[n].append(rap[n])

    # PLOTTING

    if type(fld_rng) != tuple or (type(fld_rng) == tuple and len(fld_rng) != 4):  # security - type
        print("Wrong type of field. Drawing the map is not possible.")
    else:
        # adding conversion factor and list of colors
        conv = 0.08
        colors = ['b', 'g', 'r', 'c', 'y']
        # creating an area for graphical representation
        fig, axes = plt.subplots()
        axes.set_xlim([(1 + conv) * fld_rng[0], (1 + conv) * fld_rng[1]])
        axes.set_ylim([(1 + conv) * fld_rng[2], (1 + conv) * fld_rng[3]])
        axes.set_aspect(1)

        # set size of dots depending on size of the whole area
        dot_size = (conv / 3) * min(abs(fld_rng[0] - fld_rng[1]), abs(fld_rng[2] - fld_rng[3]))
        # for each machine draw the info from each report
        for machine in positions_list:
            try:  # if too many machines, the last of them will be all in the same color
                # we can randomly pick the colors but let's leave that
                current_color = (colors.pop(0))
            except:
                current_color = "m"

            tmp = []  # temporary storage for coordinates from preceding report

            for a in machine:
                # add a dot and mark it with a report number
                draw_circle = plt.Circle(a[1], dot_size, color=current_color)
                axes.annotate(machine.index(a) + 1, xy=a[1])
                axes.add_artist(draw_circle)

                if tmp:  # for the first we dont need a line but all the other points are connected
                    if machine.index(a) == 1:  # adding a label - only once for each rocket
                        plt.arrow(*tmp, a[1][0] - tmp[0], a[1][1] - tmp[1], color=current_color,
                                  label=a[0])
                    else:
                        plt.arrow(*tmp, a[1][0] - tmp[0], a[1][1] - tmp[1], color=current_color)

                tmp = a[1]  # new temporary coordinates
        axes.legend(bbox_to_anchor=[1, 1])  # add details and print it out
        plt.title("MAP")
        plt.show()


def clearing(objs: list):
    """
    Destruct all rockets.
    :param objs: list of the machines
    """
    for _ in objs:  # destruct all objects
        del _


# RESULTS PRESENTATION

field_range = (-20, 20, -20, 20)
rockets_number = 5
moves_number = 4

rockets = initializing(Rocket, rockets_number, field_range)  # creating rockets
void_m(rockets, moves_number, field_range)  # doing the main actions
clearing(rockets)  # destructing rockets
