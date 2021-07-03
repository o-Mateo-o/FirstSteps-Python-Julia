# Task 7, list 2, WDIiP-L, PWr
# Mateusz Machaj, 29.10.2020

print('FIBONACCI\n')
n_input = input('Enter an expected number of sequence elements: ')


def fibonacci(n):
    '''
    function that gives list of fibonacci sequence elements
    :param n: number of expected sequence elements
    :return: list of fibbonacci sequence elements
    '''
    # variables initialization
    v1, v2, v_temp = 0, 1, 0
    table = []

    # in case of a wrong input there's an additional condition
    if not (n.isdigit() and 1 <= int(n)):
        return 'Incorrect number!'

    # calculating sequence terms and returning a result
    for i in range(1, int(n) + 1):
        table.append(v2)
        v_temp = v2
        v2 += v1
        v1 = v_temp
    return '%s first elements of the Fibonacci sequence: ' % n + ', '.join(map(str, table))


print(fibonacci(n_input))
