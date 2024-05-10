import numpy as np


class Accumulator:
    def __init__(self):
        self.total = 1
        self.array = [[0, 0], [0, 0], [0, 0]]

    def add(self, value):
        self.array = value
        return self.array

    def ret(self):
        tmp = [0, 1]
        for i in range(2):
            tmp[i] = self.array[1][i]
        return tmp


# Instance of Accumulator
accumulator_instance = Accumulator()


def py_set(value):
    accumulator_instance.add(value)
    return accumulator_instance.array


def py_ret(value):
    return accumulator_instance.ret()
