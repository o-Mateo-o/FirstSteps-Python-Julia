# Task 5, list 3, WDIiP-L, PWr
# Mateusz Machaj, 16.11.2020

data = [4, 2, 16, 24]  # predefined list of numbers but they can also be read from a file or console


def nat_chk(elements):
    '''
    function that tells if all elements are natural
    :param elements: list of elements to analyse
    :return: true if all elements are natural, otherwise false
    '''
    reg = []
    for el in elements:  # checking if the type is int
        if type(el) == int:
            reg.append(True)
        else:
            reg.append(False)
    for i in range(len(reg)):
        if reg[i] and not elements[i] > 0:  # positivity verification for integers
            reg[i] = False
    if False in reg:  # if there is at least one wrong value it returns false
        return False
    return True


def euclid(a, b):
    '''
    function that calculates the greatest common divisor of two numbers
    :param a: the first number
    :param a: the second number
    :return: greatest common divisor of a and b
    '''
    while b:  # simple euclidean algorithm in loop
        a, b = b, a % b
    return a


def gr_com_div(n_list):
    """
    function that calculates the greatest common divisor of the numbers from the list
    :param n_list: list of natural numbers
    :return: greatest common divisor of all the numbers
    """
    if not nat_chk(n_list):  # checking if natural using proper function
        return 0
    x = n_list[0]
    for i in n_list[1:]:  # GCD of each two following numbers
        x = euclid(x, i)
    return x


print('Finding the greatest common divisor from undermentioned list. \n'
      '(0 means that at least one element is not natural or is not a number):')
print(data)
print('Result:  ', gr_com_div(data))
