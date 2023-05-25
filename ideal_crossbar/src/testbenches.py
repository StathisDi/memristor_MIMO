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
import os
from crossbar import crossbar
import numpy as np


#############################################################
def update_sigma(sigma, start, inc, mul):
    '''
    Update sigma value for loop
    Inputs:
    sigma -> current value of sigma [float]
    start -> starting value of sigma (first iter) [float]
    inc   -> increment or multiplicand value (depending on mul) [float]
    mul   -> multiplication or addition [bool]
    Returns: next value of sigma [float]
    '''
    if start == 0.0:
        start = inc
    ret = sigma*inc if mul else sigma+inc
    ret = start if sigma == 0 else ret
    return ret


#############################################################
# Verification testbench to test the functionality of the classes
# it has no logging functionality 
def verification_tb(fast=False, test_cases=2):
    exp_times = []
    exp_rows = []
    exp_cols = []
    exp_error = []
    delta = 1.0e-12
    _Ron = 1.0e3  # in kOhm
    _Roff = 1.0e6  # in kOhm
    V_min = 0.0
    V_max = 3.0
    for i in range(test_cases):
        print("<========================================>")
        print("Test case: ", i)
        start_time = time.time()
        rows = random.randint(2,  100)
        cols = random.randint(2,  100)
        print(rows, " ", cols)
        matrix = [[random.uniform(1/(_Ron*1.0e3), 1/(_Roff*1.0e3))
                   for i in range(cols)] for j in range(rows)]
        vector = [random.uniform(V_min, V_max) for i in range(rows)]
        print("Randomized input")
        golden_model = vmm.vmm_gm(vector, matrix)
        print("Start Sim")
        if fast:
            print("Fast")
            _crossbar = crossbar("Test crossbar fast", rows, cols, False)
            cross = vmm.crossbar_fast_vmm(
                _crossbar, vector, matrix, 'custom', 0, _Ron*1.0e3, _Roff*1.0e3)
        else:
            _crossbar = crossbar("Test crossbar spice", rows, cols, True)
            cross = vmm.crossbar_vmm(
                _crossbar, vector, matrix, 'custom', 0, _Ron*1.0e3, _Roff*1.0e3)

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
# Testbench to check the variations
def variation_tb(_Ron, _Roff, _V_min, _V_max, _sigma_rel, _sigma_abs, _rep, _rows, _cols, _logs, _spice=False):
    """
    Function that implement iterative experiments in a memristor crossbar.
    It iterates over several size of crossbars (# of rows) and sigmas for absolute and relative variations.
    The results of the vmm using the crossbar is compared with the mathematical implementation.
    """
    # Ron = Ron  # 1.0e3  # in kOhm
    # Roff = Roff  # 1.0e6  # in kOhm
    # Fields in relative and absolute sigma ["start" - float, "inc" - float, "lim" - float, "mul" -  bool]
    # for 0 -> start -> start (+ or * depending on mul) incr -> up to lim
    # Fields in rows ["start" - int, "inc" - int, "lim" - int]
    # for start -> 0 + inc -> inc + inc -> up to lim
    # Fields in logs ["path" -  string, "variations" - bool, "conductance" - bool]
    cols = _cols
    for r in range(0, _rows[2], _rows[1]):
        row = _rows[0] if r == 0 else r
        sigma_rel = 0
        while sigma_rel <= _sigma_rel[2]:
            sigma_abs = 0
            while sigma_abs <= _sigma_abs[2]:
                utility.v_print_1(
                    f"rows: {row}, cols: {cols}, spice: {_spice}")
                # TODO the filename might not be required here
                file_name = str(
                    f"test_case_r_{row}_c_{cols}_abs_{sigma_abs}_rel_{sigma_rel}")
                logs = _logs + [file_name]
                # logs : {main_file_path, aux_file_path, aux_variations(bool), aux_conductance(bool), file_name}
                utility.v_print_2(f"logs {logs}")
                print("Create class")
                cross = crossbar("Test crossbar fast", row, cols, _spice, logs)
                for rep in range(0, _rep):
                    utility.v_print_2(
                        f"<===========>\nRep: {rep} \nRows: {row} \nCols: {cols} \nSigma rel: {sigma_rel} \nSigma abs: {sigma_abs}")
                    run_sim(cross, _Ron, _Roff, _V_min, _V_max,
                            sigma_rel, sigma_abs, rep, row, cols, logs, _spice)
                del cross
                sigma_abs = update_sigma(
                    sigma_abs, _sigma_abs[0], _sigma_abs[1], _sigma_abs[3])
            sigma_rel = update_sigma(
                sigma_rel, _sigma_rel[0], _sigma_rel[1], _sigma_rel[3])


#############################################################
# Run a simulation of the crossbar based on the configuration
def run_sim(_crossbar, _Ron, _Roff, _V_min, _V_max, _var_rel, _var_abs, _rep, _rows, _cols, _logs=[None, None, False, False, None], _spice=False):
    print("<========================================>")
    print("Test case: ", _rep)
    file_name = "test_case_r"+str(_rows)+"_c_" + \
        str(_cols)+"_rep_"+str(_rep)+".csv"
    file_path = _logs[0] #main file path
    header = ['var_abs', 'var_rel']
    for x in range(_cols):
        header.append(str(x))
    file = file_path+"/"+file_name # Location to the file for the main results
    # Only write header once
    if not (os.path.isfile(file)):
        utility.write_to_csv(file_path, file_name, header)
    print("<==============>")
    print("var_abs is ", _var_abs, " var_rel is ", _var_rel)
    start_time = time.time()
    print(_rows, " ", _cols)
    matrix = [[random.uniform(1/(_Ron*1.0e3), 1/(_Roff*1.0e3))
               for i in range(_cols)] for j in range(_rows)]
    vector = [random.uniform(_V_min, _V_max) for i in range(_rows)]
    print("Randomized input")
    golden_model = vmm.vmm_gm(vector, matrix)
    if _spice:
        cross = vmm.crossbar_vmm(_crossbar, vector, matrix, 'custom',
                                 0, _Ron*1.0e3, _Roff*1.0e3, _var_rel, _var_abs)
    else:
        cross = vmm.crossbar_fast_vmm(
            _crossbar, vector, matrix, 'custom', 0, _Ron*1.0e3, _Roff*1.0e3, _var_rel, _var_abs)
    error = utility.cal_error(golden_model, cross)
    data = [str(_var_abs), str(_var_rel)]
    [data.append(str(e)) for e in error]
    utility.write_to_csv(file_path, file_name, data)
    end_time = time.time()
    exe_time = end_time - start_time
    print("Execution time: ", exe_time)
