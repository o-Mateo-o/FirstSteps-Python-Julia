# Task 6, list 2, WDIiP-L, PWr
# Mateusz Machaj, 29.10.2020


print('STRINGS COMPARISON')
string_in1 = input('Enter the first string: ')
string_in2 = input('Enter the second string: ')


def str_compare(string1, string2):
    '''
    a function that compares two strings
    :param string1: first string
    :param string2: second string
    :return: list of differences and positions of them / information about equality
    '''
    # Searching for exceptions
    if string2 == '' or string1 == '':
        return 'This is not a proper string!'

    table = []
    # Checking if the lengths are equal in order to avoid errors
    length = min(len(string1), len(string2))
    if len(string1) == len(string2):
        len_equality = True
    else:
        len_equality = False
    # Comparing two strings, considering only indexes of the shorter string
    for i in range(length):
        if string1[i] != string2[i]:
            table.append(i + 1)
    # Adding that the characters of the longer string with indexes greater than length of the shorter one differ
    if not len_equality:
        for i in range(length, max(len(string1), len(string2))):
            table.append(i + 1)
    # An actual result
    if not table:
        return 'Given strings are equal.'
    else:
        return 'Given strings are different within indexes : ' + ', '.join(map(str, table)) + '  (the first is "1")'


print(str_compare(string_in1, string_in2))
