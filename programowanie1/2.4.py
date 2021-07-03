# Task 4, list 2, WDIiP-L, PWr
# Mateusz Machaj, 29.10.2020

print('CHARACTER COUNTER\n')
string_in = input('Enter a string: ')
char_in = input('Enter an expected character: ')


def char_in_str_counter(string_f, char_f):
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


print(char_in_str_counter(string_in, char_in))
# TIME TEST FOR 4 AND 5 IN ANOTHER FILE
