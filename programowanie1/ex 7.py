# Task 7, list 5, WDIiP-L, PWr
# Mateusz Machaj, 16.12.2020

import string


def anagram(word1, word2):
    """
    function that check if given list is sorted
    :param word1: first word to compare
    :param word2: second word to compare
    :return: True if they are anagrams and are words,
            False if not; ERROR if input is incorrect
    """
    # checking input (must be str, str)
    if not (isinstance(word1, str) and isinstance(word2, str)):
        return 'ERROR'
    # checking if at leas one word is an actual word
    for l in word1:
        if l not in string.ascii_letters + "'" + "-":
            return False
    # if they are not the same length, they are not anagrams
    if len(word1) != len(word2) or word1 == '':
        return False
    # creating dynamic list from second word as reference and formatted base string
    ref = list(word2.lower())
    compared = word1.lower()
    # if succeeding letters from word1 are present in word2 program deletes
    # them from the reference list and goes on
    for l in compared:
        if l in ref:
            ref.remove(l)
        else:
            return False
    return True


# results presentation:

examples = [('listen', 'silent'), ('Woda', 'oDwa'), ('Kobra', 'Bobra'), ('123', '321'),
            ('', ''), (1, 'Jo')]
for pair in examples:
    print(pair, ' -- ', anagram(pair[0], pair[1]))
