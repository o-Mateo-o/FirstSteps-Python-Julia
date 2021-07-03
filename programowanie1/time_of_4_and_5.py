# "Efficiency test" for tasks 4 and 5, list 2, WDIiP-L, PWr
# Mateusz Machaj, 29.10.2020

import time

print('TIME CHECKER FOR 4 AND 5\n')
string_in = input('Enter a string: ')
char_in = input('Enter an expected character: ')


# functions
def char_in_str_counter1(string_f, char_f):
    '''
    function that counts how many times given character figure in a string
    :param string_f: string
    :param char_f: character
    :return: quantity of expected character
    '''
    # Searching for exceptions
    if char_f == '' or string_f == '' or len(char_f) > 1:
        return 'This is not a proper string/character!'

    # counting the occurring matches
    counter = 0
    for i in range(len(string_f)):
        n = string_f.lower().find(char_f.lower(), i, i + 1)
        if n > -1:
            counter += 1
    return 'Given character occurs in the number of: ' + str(counter)


def char_in_str_counter2(string_f, char_f):
    '''
    function that counts how many times given character figure in a string
    :param string_f: string
    :param char_f: character
    :return: quantity of expected character
    '''
    # Searching for exceptions
    if char_f == '' or string_f == '' or len(char_f) > 1:
        return 'This is not a proper string/character!'

    # counting the occurring matches using .count
    return 'Given character occurs in the number of: ' + str(string_f.count(char_f))


print(char_in_str_counter1(string_in, char_in))
# actual time checking
startTime1 = time.monotonic()
for i in range(10000):
    char_in_str_counter1(string_in, char_in)
print('-------------------\nTime of execution(from task 4): ', time.monotonic() - startTime1, 's')

startTime2 = time.monotonic()
for i in range(10000):
    char_in_str_counter1(string_in, char_in)
print('-------------------\nTime of execution (from task 5): ', time.monotonic() - startTime2, 's')
