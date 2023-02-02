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

from utility import utility
from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_pΩ
import random
import time
from vmm import vmm

#############################################################


def testbench():
    test_cases = 10
    exp_times = []
    exp_rows = []
    exp_cols = []
    exp_error = []
    delta = 1.0e-12
    Ron = 1.0e3  # in kOhm
    Roff = 1.0e6  # in kOhm
    V_min = 0.0
    V_max = 3.0
    for i in range(test_cases):
        print("<========================================>")
        print("Test case: ", i)
        start_time = time.time()
        rows = random.randint(100,  2048)
        cols = random.randint(100,  200)
        print(rows, " ", cols)
        matrix = [[random.uniform(1/(Ron*1.0e3), 1/(Roff*1.0e3)) for i in range(cols)] for j in range(rows)]
        vector = [random.uniform(V_min, V_max) for i in range(rows)]
        print("Randomized input")
        golden_model = vmm.vmm(vector, matrix)
        cross = vmm.crossbar_vmm(vector, matrix, 'custom', 0, Ron*1.0e3, Roff*1.0e3)
        try:
            error = utility.compare(golden_model, cross, delta)
        except Exception as E:
            print("ERROR:")
            print("delta:", delta)
            print(E)
            exit()
        end_time = time.time()
        exe_time = end_time - start_time
        print("Execution time: ", exe_time)
        exp_times.append(exe_time)
        exp_rows.append(rows)
        exp_cols.append(cols)
        exp_error.append(max(error))
        print("<========================================>")
    avg_rows = utility.cal_average(exp_rows)
    avg_cols = utility.cal_average(exp_cols)
    avg_time = utility.cal_average(exp_times)
    avg_error = utility.cal_average(exp_error)
    print(avg_rows)
    print(avg_cols)
    print(avg_time)
    print(avg_error)

#############################################################


def main():
    util = utility(0)
    testbench()


if __name__ == "__main__":
    main()
