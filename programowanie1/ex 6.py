# Task 6, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020

def issorted(lst):
    """
    function that check if given list is sorted
    :param lst: list of elements or optionally a string
    :return: True if is sorted, False if not or is incomparable, ERROR if input is incorrect
    """
    report = []
    if not (isinstance(lst, list) or isinstance(lst, str)):
        return 'ERROR'
    # Lists without elements or having one element are sorted
    if len(lst) < 2:
        return True
    # Elements of different types are not comparable
    for i in range(0, len(lst)):
        if not isinstance(lst[i], type(lst[0])):
            return False
    # Creating a list of relations between two neighbouring elements
    # (True means >=, false =<)
    for i in range(0, len(lst)):
        if i > 0:
            if lst[i] >= lst[i - 1]:
                report.append(True)
            elif lst[i] <= lst[i - 1]:
                report.append(False)
    # Sequence is sorted only when all the relations are the same
    if all(report):
        return True
    else:
        return False


# results presentation:

examples = ['abcdefg', 'gfedcba', [1, 2, 3, 4, 5, 6], 'AbCdE', 'SIEMA!', [1], 1]
for seq in examples:
    print(seq, ' -- ', issorted(seq))
