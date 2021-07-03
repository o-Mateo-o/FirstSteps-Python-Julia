# Task 1, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020

def html_convrt(colors):
    """
    function that converts decimal RGB notation into html format
    :param colors: RGB triplet
    :return: html hex format of the triplet
    """
    parts = []
    # checking whether the type of input is proper
    if not (isinstance(colors, tuple) and len(colors) == 3):
        return 'ERROR (input type)'
    # transforming elements in loop; checking correctness of all three values in triplet
    for val in iter(colors):
        if not (str(val).isdigit() and isinstance(val, int)):
            return "ERROR (input elements)"
        elif val < 0 or val > 255:
            return "ERROR (elements range)"
        # when they are proper, then writing them in hex format as strings (without "0x")
        # if required - adding extra 0 at tke beginning
        else:
            raw_part = str(hex(val))[2:].upper()
            if len(raw_part) < 2:
                parts.append('0' + raw_part[:])
            else:
                parts.append(raw_part[:])
    # joining into html format
    html = '#' + ''.join(parts)
    return html


# results presentation:

examples = [(114, 121, 255), (0, 0, 5), (-1, 100, 200), (0.4, 12, 4), (2, 44, 21, 4), 2,
            ('a', 46, 40), ('22', '2', 4), (12, 34, 56), (256, 255, 255), (22, 46)]
for i in examples:
    print(i, "converted into:", html_convrt(i))
