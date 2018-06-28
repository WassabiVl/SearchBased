import numpy as np


class NumpyOne:
    a = np.array([1, 2, 3])
    b = np.random.uniform(0, 100, 3)
    multiply_result = np.multiply(a, b)
    dot_product = np.dot(a, b)
    cross_product = np.cross(a, b)

    @staticmethod
    def main():
        print('array A: ', *NumpyOne.a)
        print('array B:', *NumpyOne.b)
        print('Multiplication: ', *NumpyOne.multiply_result)
        print('Dot Product: ', NumpyOne.dot_product)
        print('cross Product: ', *NumpyOne.cross_product)


class NumpyTwo:
    x = np.random.rand(10, 10)
    x_determinant = np.linalg.det(x)

    @staticmethod
    def main():
        print('array x: ', *NumpyTwo.x)
        print('determinant of x: ', NumpyTwo.x_determinant)


class NumpyThree:
    input_array = np.random.randint(0, 20, 6)

    @staticmethod
    def convert_even(input_array):
        # Change elements of an array based on conditional and input values.
        np.place(input_array, (input_array % 2) == 0, input_array * -1)
        return input_array

    @staticmethod
    def main():
        # input_array = input('Array: ')
        print('input array: ', *NumpyThree.input_array)
        print('output array even converted: ', NumpyThree.convert_even(NumpyThree.input_array))


class NumpyFour:
    input_array_one = np.random.randint(0, 20, 6)
    input_array_two = np.random.randint(0, 20, 6)

    @staticmethod
    def shared_items(input_array_one, input_array_two):
        return np.intersect1d(input_array_one, input_array_two)

    @staticmethod
    def main():
        # input_array_one = input('Input Array One: ')
        # input_array_two = input('Input Array Two: ')
        print('input array one: ', NumpyFour.input_array_one)
        print('input array two: ', NumpyFour.input_array_two)
        print('shared items: ')
        print(NumpyFour.shared_items(NumpyFour.input_array_one, NumpyFour.input_array_two))
