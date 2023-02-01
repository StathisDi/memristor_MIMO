#!python3

"""
MIT License

Copyright (c) 2023 Dimitrios Stathis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Crossbar dimensions:
# Rows --> Input sources
# Columns --> Outputs during computation, ground during programming

# Calculation of Voltages depending on the state of the devices (R) and the Voltage sources

from crossbar import crossbar
from utility import utility
from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_pΩ
import numpy as np
import math
import random
import time

#############################################################


def vmm(vector, matrix):
    # Todo calculate and return the result of the vmm
    vector = np.array(vector)
    matrix = np.array(matrix).transpose()
    result = np.inner(vector, matrix)
    utility.v_print_1("vmm reference model: \n", result)
    return result

#############################################################


def translate_n_to_r(input):
    # TODO translate a number to the resistance
    r = input
    return r

#############################################################


def translate_i_to_n(input):
    # TODO translate current to number
    num = input
    return num

#############################################################


def crossbar_vmm(vector, matrix, type='custom', percentage_var=0,  Ron=1@u_pΩ, Roff=1000@u_kΩ, relative_sigma=0, absolute_sigma=0):
    # TODO calculate and return the results from the model
    result = 0
    rows = len(matrix)
    cols = len(matrix[0])
    utility.v_print_1("rows: ", rows, " cols: ", cols)
    cross = crossbar("Test crossbar", rows, cols)
    cross.update_device_type(type, percentage_var,  Ron, Roff, relative_sigma, absolute_sigma)
    cross.create_netlist()
    print("Created netlist")
    sources = [u_V(vector[y]) for y in range(rows)]
    res = [[] for y in range(rows)]
    for y in range(rows):
        res[y] = [u_Ω(1/translate_n_to_r(matrix[y][x])) for x in range(cols)]
    utility.v_print_2("Sources based on input vector: \n", sources)
    utility.v_print_2("Resistances based on input matrix: \n", res)
    cross.set_sources(sources)
    cross.update_all_devices(res)
    print("Sources and device state is updated")
    cross.circuit_solver()
    o_current = cross.get_current()
    utility.v_print_1("Read currents: \n", o_current)
    result = [translate_i_to_n(float(i)) for i in o_current]
    return result

#############################################################


def compare(reference, modeled, delta):
    # TODO compare the two results
    error = reference - modeled
    if any(abs(x) > delta for x in error):
        print(reference)
        print(modeled)
        print(error)
        raise Exception("Large error: \n", error)
    return error

#############################################################


def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg

#############################################################


def main():
    util = utility(0)
    test_cases = 100
    exp_times = []
    exp_rows = []
    exp_cols = []
    exp_error = []
    exp_delta = []
    delta = 0.00001
    flag = 0
    f_error = None
    f_delta = 0
    for i in range(test_cases):
        print("<========================================>")
        print("Test case: ", i)
        start_time = time.time()
        delta = delta/2
        rows = random.randint(2,  4*2048)
        cols = random.randint(2,  200)
        print(rows, " ", cols)
        matrix = [[random.uniform(1, 1000) for i in range(cols)] for j in range(rows)]
        # matrix = [[1, 2], [5, 3], [4, 1]]
        # vector = [2, 7, 3]
        vector = [random.uniform(1, 1000) for i in range(rows)]
        print("Randomized input")
        golden_model = vmm(vector, matrix)
        check = golden_model+0.00011
        # print("Golden model: \n", golden_model)
        cross = crossbar_vmm(vector, matrix, 'custom')
        # print("Modeled: \n", cross)
        try:
            error = compare(golden_model, cross, delta)
            exp_error.append(error)
        except Exception as E:
            if flag == 0:
                f_error = E
                f_delta = delta
                flag = 1
            exp_error.append(E)
            print("ERROR:")
            print(delta)
            print(E)
        end_time = time.time()
        exe_time = end_time - start_time
        print("Execution time: ", exe_time)
        exp_times.append(exe_time)
        exp_rows.append(rows)
        exp_cols.append(cols)
        exp_delta.append(delta)
        print("<========================================>")
    print(exp_rows)
    print(exp_cols)
    print(exp_times)
    avg_rows = cal_average(exp_rows)
    avg_cols = cal_average(exp_cols)
    avg_time = cal_average(exp_times)
    print(avg_rows)
    print(avg_cols)
    print(avg_time)
    print("Error gen: ", flag)
    print(f_error)
    print(f_delta)
    # try:
    #    cross.set_sources([20@u_V, 20@u_V, 20@u_V, 20@u_V, 20@u_V, 20@u_V])
    # except Exception as E:
    #    print(E)


if __name__ == "__main__":
    main()
