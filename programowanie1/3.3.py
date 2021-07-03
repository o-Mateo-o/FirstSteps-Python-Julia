# Task 3, list 3, WDIiP-L, PWr
# Mateusz Machaj, 16.11.2020

def encod_rot13(text):
    """
    this function encodes given text using ROT13 (servicing only standard latin letters)
    :param text: text from console
    :return: converted text
    """
    text13 = []
    # creating reference lists to transform each character
    letters_std = list(range(ord('a'), ord('z')+1))              # lower case letters
    letters_std.extend(list(range(ord('A'), ord('Z')+1)))         # adding upper case
    letters13 = letters_std[13:26]                  # then making a list of corresponding ROT13 letters
    letters13.extend(letters_std[0:13])
    letters13.extend(letters_std[39:52])
    letters13.extend(letters_std[26:39])
    reference_std = ''.join(map(chr, letters_std))  # put it into string to make searching comfortable
    reference13 = ''.join(map(chr, letters13))
    # encoding given text (changing only latin letters)
    for a in text:
        if a in reference_std:
            text13.append(reference13[reference_std.find(a)])
        else:
            text13.append(a)
    # put it back into string and return
    return ''.join(text13)

print(ord('a'), ord('z'))

print('Standard ROT13 converter (services only latin alphabet)')
content = input('Enter your text to encode: ')
print('Converted text:  ', encod_rot13(content))
