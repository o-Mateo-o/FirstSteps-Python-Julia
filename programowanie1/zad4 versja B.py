import math

r_input = input('podaj promień: ')

def volume(r):
    r_float = float(r)
    return((4/3)*math.pi*pow(r_float,3))

print(volume(r_input))
