table_1 = [1, 2, 3, 4]
table_2 = [1, 3, 5, 3, 5, 3, 5, 1, 1]

def printer(table, align):
    # align can be left-"L" or center-"C"
    if align == "L":
        for i in table:
            for j in range(0, i):
                print("*", end='')
            print('')
    if align == "C":
        width = max(table)
        for i in table:
            for k in range(0, (width - i) // 2):
                print(" ", end='')
            for j in range(0, i):
                print("*", end='')
            print('')
    print('')


printer(table_1, "L")
printer(table_2, "C")
