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

from crossbar import crossbar
from utility import utility
from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_pΩ
import numpy as np
# import cupy as cp
import gc

# Class that defines the vmm functions


class vmm:

    #############################################################

    def vmm_gm(vector, matrix):
        '''
        Basic matrix vector multiplication
        '''
        # if utility.gpu:
            #     vector = cp.array(vector)
            #     matrix = cp.array(matrix).transpose()
            #     result = cp.inner(vector, matrix)
            # else:
            #     vector = np.array(vector)
            #     matrix = np.array(matrix).transpose()
            #     result = np.inner(vector, matrix)
        vector = np.array(vector)
        matrix = np.array(matrix).transpose()
        result = np.inner(vector, matrix)
        utility.v_print_1("vmm reference model: \n", result)
        return result

    #############################################################

    def crossbar_vmm(cross, vector, matrix, type='custom', percentage_var=0,  Ron=1@u_pΩ,    Roff=1000@u_kΩ,    relative_sigma=0, absolute_sigma=0):
        '''
        Run the memristor simulation for the vector matrix multiplication
        '''
        result = 0
        rows = len(matrix)
        cols = len(matrix[0])
        # utility.v_print_1("rows: ", rows, " cols: ", cols)
        # cross = crossbar("Test crossbar", rows, cols, True, logs)
        cross.update_device_type(type, percentage_var,  Ron, Roff, relative_sigma, absolute_sigma)
        cross.create_netlist()
        print("Created netlist")
        sources = [u_V(vector[y]) for y in range(rows)]
        res = [[] for y in range(rows)]
        for y in range(rows):
            res[y] = [u_Ω(utility.translate_input(1/matrix[y][x], 1.0)) for x in range(cols)]
        utility.v_print_2("Sources based on input vector: \n", sources)
        utility.v_print_2("Resistances based on input matrix: \n", res)
        cross.set_sources(sources)
        cross.update_all_devices(res)
        print("Sources and device state is updated")
        o_current = cross.sim()
        # = cross.get_current()
        utility.v_print_1("Read currents: \n", o_current)
        result = [utility.translate_output(float(i), 1.0) for i in o_current]
        gc.collect()
        return result

    #############################################################

    def crossbar_fast_vmm(cross, vector, matrix, type='custom', percentage_var=0,  Ron=1@u_pΩ,    Roff=1000@u_kΩ,    relative_sigma=0, absolute_sigma=0):
        '''
        Run the memristor simulation for the vector matrix multiplication
        '''
        result = 0
        rows = len(matrix)
        cols = len(matrix[0])
        print("Update device")
        cross.update_device_type(type, percentage_var,  Ron, Roff, relative_sigma, absolute_sigma)
        print("Create netlist")
        cross.create_netlist()
        print("Created netlist")
        sources = [u_V(vector[y]) for y in range(rows)]
        res = [[] for y in range(rows)]
        for y in range(rows):
            res[y] = [u_Ω(utility.translate_input(1/matrix[y][x], 1.0)) for x in range(cols)]
        utility.v_print_2("Sources based on input vector: \n", sources)
        utility.v_print_2("Resistances based on input matrix: \n", res)
        print("Set sources")
        cross.set_sources(sources)
        print("Update devices")
        cross.update_all_devices(res)
        print("Sources and device state is updated")
        o_current = cross.sim()
        # o_current = cross.get_current()
        utility.v_print_1("Read currents: \n", o_current)
        result = [utility.translate_output(float(i), 1.0) for i in o_current]
        return result

    #############################################################

    def crossbar_sim_vmm(cross, vector, matrix, type='custom', percentage_var=0,  Ron=1@u_pΩ,    Roff=1000@u_kΩ,    relative_sigma=0, absolute_sigma=0):
        '''
        Run the memristor simulation for the vector matrix multiplication
        '''

        # Vector to Voltage

        # Matrix to memristor

        # Crossbar read

        # Current to result
        
        return result
