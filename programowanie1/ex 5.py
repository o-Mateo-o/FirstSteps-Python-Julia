# Task 5, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020

import string


def palindrome(word):
    """
    function that checks if given word is a palindrome
    :param word: word to examine
    :return: True if it is, False if is not a word or is a word but not palindrome
    """
    # creating two character sequences - normal and reversed
    w_normal = word.lower()
    w_rever = word[::-1].lower()
    # checking if the input is an actual word
    for l in w_normal:
        if l not in string.ascii_letters + "'" + "-":
            return False
    # if it is a word check if it is a palindrome (true means it is)
    return True if w_normal == w_rever else False


# results presentation:

examples = ['Palindrome', 'kayak', 'MulUm', '7uo', 'Oo - oO', 'Kobyła ma mały bok']
for elem in examples:
    print(elem, '-- is a palindrome word.' if palindrome(elem) else '-- is not a palindrome word.')
