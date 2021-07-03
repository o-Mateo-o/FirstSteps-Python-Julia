# Task 1, list 3, WDIiP-L, PWr
# Mateusz Machaj, 16.11.2020

import matplotlib.pyplot as plt


def letter_freq_graph(text):
    """
    this function makes a bar graph of a letter frequency in a given document
    :param text: content of a file - some text
    it's a void function
    """
    inventory = dict()
    report_val = []
    report_let = []
    # putting all the letters along with their number down to the dictionary
    for letter in list(map(chr, range(97, 123))):
        inventory.update({letter: text.lower().count(letter)})
    # choosing 10 most popular letters and creating two lists for axes
    for let in sorted(inventory, key=inventory.get, reverse=True):
        if len(report_val) < 10:
            report_let.append(let.upper())
            report_val.append(inventory[let])
    # creating an actual bar graph
    plt.bar(report_let, report_val)
    plt.title('Letter frequency - ENGLISH')
    for x, y in zip(report_let, report_val):
        # adding value labels to the bars
        label = "{:.0f}".format(y)
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, -15), ha='center')
    # showing a final effect
    plt.show()

    # opening file and analysing its content in order to print out a graph


try:
    file = open('source.txt', 'r')
    content = file.read()
    letter_freq_graph(content)
except:
    print('File Error')
