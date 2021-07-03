# Task 3 and 4, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020
import time
import matplotlib.pyplot as plt
import numpy as np


def fibonacci_iter(n):
    """
    function that gives a list of fibonacci sequence elements (BY ITERATION)
    :param n: number of expected sequence elements
    :return: n element of Fibonacci sequence
    """
    # variables initialization
    v1, v2, v_temp = 0, 1, 0

    # in case of a wrong input there's an additional condition
    if not isinstance(n, int):
        return False
    if n <= 0:
        return False

    # calculating sequence terms and returning a result
    for i in range(2, int(n) + 1):
        v_temp = v2
        v2 += v1
        v1 = v_temp
    return v2


def fibonacci_rec(n):
    """
    function that gives a list of fibonacci sequence elements (BY RECURSION)
    :param n: number of expected sequence elements
    :return: n element of Fibonacci sequence
    """
    # check if proper input
    if not isinstance(n, int):
        return False
    if n <= 0:
        return False
    # simple recursion
    if n <= 1:
        return n
    else:
        return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


# ------------------------------------------------------------------
# results presentation:




def exec_time(function, elems):
    """
    function that measures function's time of execution
    :param function: function working on some number of natural elements
    :param elems: number of elements (natural)
    :return: list of results for each integer
    """
    report = []
    for i in range(1, elems + 1):
        start = time.perf_counter_ns()
        function(i)
        stop = time.perf_counter_ns()
        report.append(stop - start)
    return report


def plot_printer(fnct_lst, meth_names, rng):
    """
    void function that creates a plot for functions and writes down some conclusions
    :param fnct_lst: list of functions
    :param meth_names: names to identify each function
    :param rng: range to work on (integer)
    """
    print('Time of execution for the maximal number of elements in range: ')
    for j in range(0, len(fnct_lst)):
        colors = ['red', 'blue']
        # creating arrays for each axis
        times = exec_time(fnct_lst[j], rng)
        absc = np.linspace(0, rng, rng)
        ordins = np.asarray(times)
        # plotting a graph for current function and printing the time of execution for the maximal element
        plt.plot(absc, ordins, 'o', color=colors[j], label=meth_names[j])
        print(meth_names[j], ': ', times[-1], ' ns')
    # Describing
    plt.title('Execution time of different methods.', fontdict=None, loc='center', pad=None)
    plt.xlabel('Number of elements')
    plt.ylabel('Time [ns]')
    plt.legend()
    plt.show()


# calling a function above to see the result
n = 30  # number of expected elements

examples = [-1, 0.5, 3, 'a', 6]
print('Iterative - examples:')
for i in examples:
    print(i, " -- ", fibonacci_iter(i))
print('Recursive - examples:')
for i in examples:
    print(i, " -- ", fibonacci_rec(i))
plot_printer([fibonacci_iter, fibonacci_rec], ['iteratively', 'recursively'], n)
