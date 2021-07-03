# Task 3, list 2, WDIiP-L, PWr
# Mateusz Machaj, 29.10.2020

print('CHARACTER FINDER - PREMIUM\n')
string_in = input('Enter a string: ')
char_in = input('Enter an expected character: ')
# ADJUSTMENT !!!!!!!!!
index_in = input('Enter an initial index (the first is "1"): ')


def char_finder(string_f, char_f, index_f):
    '''
    function that finds given character in a string with possibility to start from given index
    :param string_f: string
    :param char_f: character
    :param index_f: index to start searching from
    :return: information about character presence and its positions if it is found
    '''
    # Searching for exceptions
    # ADJUSTMENT !!!!!!!
    try:
        int(index_f)
    except:
        return 'Given index is not a number!'
    if int(index_f) < 1:
        return 'This is not a proper index!'

    if char_f == '' or string_f == '' or len(char_f) > 1:
        return 'This is not a proper string/character!'

    # checking each char in given string in order to find a mach, then write it down in the table when found
    table = []
    # ADJUSTMENT !!!!!!!!!!!
    for i in range(int(index_f) - 1, len(string_f)):
        n = string_f.lower().find(char_f.lower(), i, i + 1)
        if n > -1:
            table.append(n + 1)

    # preparing an output
    # in case there is no mach
    if len(table) == 0:
        return 'There is no such character.'
    # typical result
    else:
        return 'Position of a given character:  ' + ', '.join(map(str, table)) + '  (the first is "1")'


# (adjustment)
print(char_finder(string_in, char_in, index_in))
