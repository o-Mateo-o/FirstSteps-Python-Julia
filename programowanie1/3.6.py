# Task 6, list 3, WDIiP-L, PWr
# Mateusz Machaj, 16.11.2020


def nat_chk(element):
    '''
    function that tells if an element is natural
    :param element: an element to analyse
    :return: true if an element is natural
    '''
    if element.isnumeric() and int(element)>0:
        return True
    else:
        return False


def pascal(rows_raw):
    """
    function that writes down into table required number of pascal's triangle rows
    :param rows_raw: number of rows
    :return: pascal's triangle in a table
    """
    if rows_raw.isnumeric() and int(rows_raw)>0:
        rows = int(rows_raw)
        table = []
        for line in range(rows):  # creating each row in te table
            table.append([])
            table[line].append(1)  # the first value is 1 in each row
            for pos in range(1, line):
                # having the first value it starts computing following values (beginning from the second)
                # new value is a sum of two values from previous line - the one with preceding index and this
                # with index equal to this being created
                table[line].append(table[line - 1][pos - 1] + table[line - 1][pos])
            if line > 0:  # additional 1 ending each line (except the first)
                table[line].append(1)
        return table
    else:
        return []


def printer(tab):
    """
    void function that prints out a centred table
    :param tab: table which we want to center and print
    """
    if tab:
        width = len('   '.join(map(str, tab[-1])))  # defining width - maximal length of a line (along with spacing)
        for i in range(len(tab)):  # making each aline centered (+ adding proper spacing)
            print('   '.join(map(str, tab[i])).center(width))
    # really legible result ...for not too huge number of rows :P
    else:
        print('Wrong input.')


print('Pascal\'s triangle.')
numb = input('Enter desired number of rows:  ')
printer(pascal(numb))



