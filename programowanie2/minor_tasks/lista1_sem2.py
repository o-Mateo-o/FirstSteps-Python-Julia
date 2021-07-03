# List 1, Prog.-L, PWr
# Mateusz Machaj, 02.03.2021

# within the module I will mark lines/blocks not mensioned in the task with a comment "# ADDITIONAL IDEA"


'''
A module thet contains a custom vector class with basic operations and presentation.
Class tests are placed in the external file
'''


import random
import math


class Vector:
    '''vector class with basic operations
    the main attribute is ::self.components:: which stores a list of components (floats or ints)
    can be constructed by giving a dimension or a list of components as an argument
    '''
    def __list_to_vect(self, elements):
        '''helper function
        save given values in self.components assuming that proper list is on input
        ::param elements:: (list) of elements - needed the len as vector
        '''
        # checking for types inside the list using a "reduction" method
        if len([elem for elem in elements if type(elem) not in {float, int}]) > 0:
            raise ValueError("list includes non-numeric values")
        self.components = elements

    # NOTE: n isn't really suitable name for a variable that can possibli be a list 
    # but I had to change it from "paramet" in order to match with your convention

    def __init__(self, n: int = 3):
        '''construct a null vector with given size xor given components and savig it in attribute self.components
        ::param n:: (int) - by deafult - or (list) of numbers - "overloaded" constructor
        '''
        if type(n) == int:
            if n <= 0:
                raise ValueError("dimension should be positive")
        # ADDITIONAL IDEA - to have a "specified" vector in advance,
        # plus 'overloading' to let the user specify values in the vector when initializing
            self.components = [0] * n

        elif type(n) == list:
            if len(n) <= 0:
                raise ValueError("dimension should be positive")
            self.__list_to_vect(n)
    
        self.n = n

    def __mul__(self, scalar: float):
        '''operation of multiplication by a scalar
        ::param scalar:: (int or float) a scalar
        ::return:: (Vector) result of standard scalar multiplication
        '''
        if type(scalar) not in {int, float}:
            raise TypeError("not a scalar")
        else:
            new_vect = Vector(len(self)) # creating new vector to return a proper type
            new_vect.from_list([comp*scalar for comp in self.components])
            return new_vect
    
    def __rmul__(self, scalar: float):
        '''operation of reversed multiplication by a scalar - defined by multiplication by a scalar
        ::param scalar:: (int or float) a scalar
        ::return:: (Vector) result of standard scalar multiplication
        '''
        return self*scalar

    def __add__(self, other):
        '''operation of vector addition
        ::param other:: (Vector) another vector - the same dimension expected
        ::return:: (Vector) result of standard vector addition
        '''
        if type(other) != type(self):
            raise TypeError(
                "you can add to (subtract from) a vector only an object of the same type")
        else:
            if len(other) == len(self):
                elems_tmp = []
                for i in range(0, len(self)):
                    elems_tmp.append(self.components[i]+other.get_list()[i])
                new_vect = Vector(len(self)) # creating new vector to return a proper type
                new_vect.from_list(elems_tmp)
                return new_vect
            else:
                raise ValueError("wrong input dimension")

    def __sub__(self, other):
        '''operation of vector subtraction
        ::param other:: (Vector) the second vector - the same dimension expected
        ::return:: (Vector) result of standard vector subtraction
        '''
        return self + other*(-1) # '-' defined by using '+' and scalar '*'

    def __str__(self) -> str:
        '''show the string representation of a self.components list
        ::return:: (str) string representation of components
        '''
        return str(self.components)

    def __getitem__(self, index: int):
        '''[] operator
        ::return:: (float or int) component of a given index
        '''
        if type(index) != int:
            raise ValueError()
        try:
            return self.components[index]
        except IndexError:
            raise IndexError("vector index out of range")

    def __contains__(self, elem: float) -> bool:
        '''is operator - check if the element is a component
        ::param elem:: (float or int) element to examine
        ::return:: (bool) inormation about element's presence whithin vector components
        '''
        return elem in self.components

    # ADDITIONAL IDEA

    def __len__(self) -> int:
        '''len operetor - give a vector's dimension
        ::return:: (int) dimension of a vector 
        '''
        return len(self.components)

    # ADDITIONAL IDEA

    def __eq__(self, other) -> bool:
        '''== operator - check if two vectors have the same elements on the same positions
        ::param other:: (Vector) a vector to compare
        ::return:: (bool) information about equality
        '''
        if type(other) != type(self):
            raise TypeError("non-comparable")
        if len(other) != len(self):
            return False

        elems_ev = []
        for i in range(0, len(self)):
            # comparing on each index
            elems_ev.append(
                True if self.components[i] == other.get_list()[i] else False)

        if False in elems_ev:
            return False
        else:
            return True

    # ADDITIONAL IDEA - "get" function

    def get_list(self) -> list:
        '''get a a list of components 
        ::return:: (list) components
        '''
        return self.components

    def random_values(self, low: float = -10, high: float = 10, integer_only: bool = False):
        '''fill self.components with random values from a given range
        ::param low:: (int) lower boundary of random generating
        ::param high:: (int) upper boundary of random generating
        ::param low:: (bool) optional only-integer flag
        '''
        try:
            low = float(low)
            high = float(high)
        except:
            raise ValueError("boundaries are expected to be numbers")
        if low > high:
            raise Exception("boundaries should be reversed")

        if integer_only == True:
            self.components = [random.randrange(
                math.ceil(low), math.ceil(high)) for comp in self.components]
        else:
            self.components = [random.uniform(
                low, high) for comp in self.components]

    def from_list(self, new_compon: list = []):
        '''fill self.components with values from a given list
        ::param new_compon:: (list of ints or floats) list of new vector values - the same dimension expected
        '''
        if type(new_compon) != list:
            raise TypeError("input type for update sholud be list")
        if len(new_compon) == len(self):
            self.__list_to_vect(new_compon)
        else:
            raise ValueError("wrong input dimension")

    def by_scalar(self, scalar: float):
        '''multiply by a scalar
        ::param scalar:: (int or float) a scalar
        ::return:: (Vector) result of standard scalar multiplication
        '''
        return self*scalar

    def vec_len(self) -> float:
        '''give the length of a vector
        ::return:: (float) vector length 
        '''
        return float(math.pow(sum([comp**2 for comp in self.components]), 1/2))

    def elem_sum(self) -> float:
        '''give the sum of components
        ::return:: (float) sum of components
        '''
        return float(sum([comp for comp in self.components]))

    # NOTE: Multiplication operator is not overloaded to service dot product, 
    # because of the difference in written symbols of theese operations.

    def scalar_prod(self, other) -> float:
        '''give a result of vectors dot product
        ::param other:: (Vector) the second vector - the same dimension expected
        ::return:: (float) standard dot product
        '''
        if type(other) != type(self):
            raise TypeError("dot product is possible only with two vectors")
        else:
            if len(other) == len(self):
                elems_tmp = []
                for i in range(0, len(self)):
                    elems_tmp.append(self.components[i]*other.get_list()[i])
                return float(sum(elems_tmp))
            else:
                raise ValueError("wrong input dimension")


if __name__ == "__main__":

    # PRESENTATION

    def presentation():
        v = Vector([10, 20, 10])
        print("v:", v)
        try:
            v.from_list([1, "a"])
        except:
            print("Exception there - not proper dim and types.")
        v.from_list([1, 2, 3])
        print("v after update:", v)
        w = Vector(3)
        w.random_values(-10, 10)
        print("w:", w)
        print("w+v:", v+w)
        print("w-v:", v-w)
        print("5*v:", v*5, "=", v.by_scalar(5))
        print("v o w:", v.scalar_prod(w))
        print("v[0]:", v[0])
        try:
            v[8]
        except:
            print("Exception there - index 8 is out of range.")
        print("len(v):", len(v))
        print("1 and 4 in v:", 1 in v, "and", 4 in v)
        print("v length:", v.vec_len())
        print("v sum of components:", v.elem_sum())
        print("w and v equality:", v == w)
        w.from_list([1, 2, 3])
        print("w and v equality after [1,2,3] update:", v == w)
        print("get v:", v.get_list(), type(v.get_list()))


        # CLASS TESTS by Anna Szymanek in external file
