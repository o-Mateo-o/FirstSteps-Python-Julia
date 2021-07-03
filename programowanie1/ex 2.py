# Task 2, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020

def rgb_convrt(colors):
    """
    function that converts html color format into decimal RGB notation
    :param colors: html format
    :return: decimal RGB triplet
    """
    elms = []
    # checking whether the type of input is proper
    if not (isinstance(colors, str) and len(colors) == 7 and colors[0] == '#'):
        return 'ERROR (input type)'
    parts = [colors[1:3], colors[3:5], colors[5:7]]
    # transforming elements in loop; if they ar not correct, return exception
    for val in iter(parts):
        try:
            elms.append(int("0x" + val, 16))
        except:
            return "ERROR (sequence characters)"
    # reformat our list into a tuple
    return tuple(elms)


# results presentation:

examples = ['#FA0245', '#FFf625', 'DDf625', '#011', '#-10234', '#gr9887']
for i in examples:
    print(i, "converted into:", rgb_convrt(i))
