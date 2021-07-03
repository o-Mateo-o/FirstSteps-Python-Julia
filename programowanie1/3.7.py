# Task 7, list 3, WDIiP-L, PWr
# Mateusz Machaj, 16.11.2020

print('ax^2+bx+c is a quadratic equation.')
a1 = input('Enter a: ')
b1 = input('Enter b: ')
c1 = input('Enter c: ')


def trinomial(a_raw, b_raw, c_raw):
    """
    function that solves quadratic equations in real numbers
    :param a_raw: first coefficient
    :param b_raw: second coefficient
    :param c_raw: third coefficient
    :return: solutions or info about lack of solutions
    """
    try:  # transforming data into float type
        a, b, c = float(a_raw), float(b_raw), float(c_raw)
    except:
        return 'ERRRORRRR! Wrong values!'  # + check if number
    if a == 0:  # when it is "ax+b"
        if b == 0:  # when constant
            if c == 0:
                return 'each x'
            return '-'
        return -b / a  # linear, not constant
    dl = (b ** 2 - 4 * a * c)  # delta
    if dl < 0:  # when negative there is no solution
        return '-'
    elif dl == 0:  # one when equals 0
        return -b / (2 * a)
    sqrt_dl = dl ** 0.5  # otherwise compute square root of delta and give solutions
    return (-b - sqrt_dl) / (2 * a), (-b + sqrt_dl) / (2 * a)


print('Real solutions of the equation: ')
print(trinomial(a1, b1, c1))
