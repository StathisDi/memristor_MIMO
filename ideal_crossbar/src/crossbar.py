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


import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_MΩ, u_pΩ
from memristor import memristor
import numpy as np
import cupy as cp
import random
import re
from utility import utility


# 1 Class for the Crossbar
#   Is build as a spice netlist using pyspice
#   Comprises from resistances in a nxm crossbar, where the n is the input rows and m the output
#   Has a solver
class crossbar:

    ###################################################################################
    def __init__(self, name="", rows=0, cols=0, spice=False, logs=[None, False, False, None], R_read=None, R_read_var=None):
        '''
        Constructor
        Inputs:
          - name (string)
          - rows, cols: dimensions of the crossbar (integer)
          - R_read: read resistance (Float)
          - R_read_var: variations in the read resistance (Float < 1)
          - spice: Boolean value that specifies if spice simulation will run. If False R_read and _var are ignored (default False)
          - logs: Array of system path and 2 boolean values (Default [None, False, False])
        '''
        utility.v_print_1("Creating crossbar!\n")
        self.name = name
        self.rows = rows
        self.cols = cols
        self.inputs = rows
        self.outputs = cols
        self.elements = rows*cols
        self.spice = spice
        # Devices
        self.devices = [[memristor(((cols*y)+x), rows, cols, 'ideal', 0, 1@u_pΩ, 10000@u_MΩ, 0.0, 0.0, logs) for x in range(cols)] for y in range(rows)]
        # self.devices = [[print((cols*y)+x) for x in range(cols)] for y in range(rows)]
        print("Devices")
        self.device_state = [
            [self.devices[y][x].R for x in range(cols)] for y in range(rows)]
        # Input
        self.sources_values = [1@u_V for y in range(rows)]
        # Output
        self.I_outputs = [0@u_A for x in range(cols)]
        # Flag for spice netlist
        self.netlist_created = 0
        # lists of spice elements
        self.res = []
        self.read_res = []
        self.sources = []
        self.currents = []
        self.voltages = []
        self.read_node_str = [str(x)+"_grd" for x in range(cols)]

        utility.v_print_2("Read_nodes: \n", self.read_node_str, "\n")

        if R_read_var == None:
            self.R_read_var = [0 for x in range(cols)]
            utility.v_print_1(
                "R variations is not defined, 0% variations will be used!")
        else:
            self.R_read_var = R_read_var

        if not (any((0 <= x <= 1) for x in self.R_read_var)):
            raise Exception("R read variations should be in range [0,1]!")

        if R_read == None:
            self.R_read = [0.0000000000000000000001@u_pΩ for x in range(cols)]
            utility.v_print_1(
                "R_read is not defined, 0.0000000000000000000001 pΩ value will be used!")
        else:  # assign values to R read including variation
            self.R_read = [(r+r*random.uniform(0, x))
                           for x in self.R_read_var for r in R_read]

        utility.v_print_1(
            "\n\nInitialization of the crossbar setup completed!\n\n")

    ###################################################################################
    def __str__(self):
        return f"{self.name}: rows:{self.rows}, cols:{self.cols}, elements:{self.elements}, spice:{self.spice}"

    ###################################################################################
    def update_device_type(self, device='ideal', percentage_var=0,  Ron=1@u_kΩ, Roff=1000@u_kΩ, relative_sigma=0, absolute_sigma=0):
        '''
        Update the type of all devices in the crossbar

        Inputs:
          - device='ideal': device type (string: 'ideal', 'ferro', 'MF/SI', 'custom')
          - percentage_var=0 : percent device to device variation (float <1)
          - Ron=1@u_kΩ, Roff=1000@u_kΩ : Ron and Roff values (u_Ω spice unit)
          - relative_sigma=0, absolute_sigma=0 : Write/Read variation (float <1)
        '''
        for r in self.devices:
            for i in r:
                i.set_device_type(device, percentage_var, Ron,
                                  Roff, relative_sigma, absolute_sigma)

    ###################################################################################
    def print_device_coordinates(self):
        '''
        Print the coordinates of all devices in the crossbar
        '''
        for y in range(self.rows):
            for x in range(self.cols):
                print(self.devices[y][x].coordinates, "=",
                      self.device[y][x].resistance, end=" ")
            print("")

    ###################################################################################
    def print_netlist(self):
        '''
        Detail print of the netlist, sources and resistances
        '''
        if (self.netlist_created == 1) and self.spice:
            for y in range(self.rows):
                print(self.sources[y], end=" --> ")
                for x in range(self.cols):
                    print(self.res[y*self.cols+x].resistance, end=" ")
                print("")
            print("Read resistances: ")
            [print(self.read_res[x]) for x in range(self.cols)]
            print(self.circuit)
        else:
            raise Exception(
                "Netlist has not been created or spice simulation is set to false (self.spice)!")

    ###################################################################################
    def detail_print(self):
        '''
        Print all info about the class
        '''
        print(self.name, ":")
        print(f"\t Rows: {self.rows}")
        print(f"\t Columns: {self.cols}")
        print(f"\t Inputs: {self.rows}")
        print(f"\t Outputs: {self.cols}")
        print(f"\t Elements: {self.elements}")
        print(f"\t Device state: ")
        for y in range(self.rows):
            print(self.device_state[y])
        print("\t Sources:")
        print(self.sources_values)
        print("\t Current output:")
        print(self.I_outputs)
        print(f"Spice flag {self.spice}")

    ###################################################################################
    def fast_sim(self):
        '''
        Run a fast simulation (without spice) of the crossbar, it only implements the vector matrix multiplication

        The function is implemented as a vector matrix multiplication between the sources and the conductance values
        of the devices in the crossbar
        '''
        if self.netlist_created == 1 and self.spice == False:
            print("Fast sim!")
            vector = [float(i.dc_value) for i in self.sources]
            matrix = [[float(1/self.devices[y][x].R)
                       for x in range(self.cols)] for y in range(self.rows)]
            if utility.gpu:
                vector = cp.array(vector)
                matrix = cp.array(matrix).transpose()
                result = cp.inner(vector, matrix)
            else:
                vector = np.array(vector)
                matrix = np.array(matrix).transpose()
                result = np.inner(vector, matrix)
            utility.v_print_1("Fast mem model: \n", result)
        else:
            raise Exception(
                f"ERROR [fast_sim  {self.name} ]! There is no defined netlist!")

        return result

    ###################################################################################
    def set_sources(self, v):
        '''
        Set values for all the sources in the crossbar
        Input:
          - v: Vector with the values of each source, has to be the same height as the rows
        '''
        self.sources_values = v
        if (self.sources.__len__() != v.__len__()):
            raise Exception(
                "Input vector of sources, not equal size as the number of sources!")

        if self.netlist_created == 1:
            for y in range(self.rows):
                self.sources[y].dc_value = v[y]
            utility.v_print_1("Netlist is updated!")
        else:
            utility.v_print_1(
                "Source values are updated, waiting to create netlist!")

    ###################################################################################
    def print_sources(self):
        '''
        Print the circuit sources
        '''
        if self.netlist_created == 1:
            print("Defined sources in the circuit: ", self.circuit.title)
            for source in self.sources:
                print(source)
        else:
            print("There is no netlist created!")

    ###################################################################################
    def get_current(self):
        '''
        Get current values per branch
        '''
        if self.netlist_created == 0 or self.spice == False:
            raise Exception(
                f'Function \"get_current\" in {self.name} should not be called when spice is set to False')
        # The first row currents are from the sources (negative), the rest are from the resistors
        # The name conventions (i.e. str format) is Branch vr0_plus for resistors and v9 for sources
        self.I_outputs = [i[0]
                          for i in self.currents if re.match(r"vr", i._name)]
        [utility.v_print_2(f"Name: {str(i)} Value: {float(i)}")
         for i in self.currents]
        utility.v_print_1("Calculated outputs:")
        utility.v_print_1(self.I_outputs)
        return self.I_outputs

    ###################################################################################
    def update_device(self, x, y, target_resistance):
        '''
        Updates the internal state of a device in node [y,x] with a given resistance.
        It updates the memristor element and the spice netlist

        Inputs:
          - x,y : coordinates
          - Resistance to be programmed
        '''
        utility.v_print_2(
            "Updating device resistance. Device: [", y, ",", x, "]")
        if not ((0 <= y < self.rows) and (0 <= x <= self.cols)):
            raise Exception(f"Try to access device with out of bounds coordinates.\nGiven coordinates: \
                            [{str(y)},{str(x)}]. Valid coordinate range y: [0,{str(self.rows-1)}] range of x: [0,{str(self.cols-1)}]")
        self.devices[y][x].update_state(target_resistance)
        self.device_state[y][x] = self.devices[y][x].R
        index = y*self.cols+x  # Translate the 2D index to the vector index of the netlist
        if self.netlist_created == 1:
            if self.spice:
                self.res[index].resistance = self.devices[y][x].R
            utility.v_print_2("Resistances in netlist is updated!")
        else:
            utility.v_print_2(
                "Resistance values are updated, waiting to create netlist!")

    ###################################################################################
    def update_all_devices(self, resistance_matrix):
        '''
        Updated all devices

        Inputs:
          - Matrix the size of the crossbar with the target resistance values
        '''
        # resistance_matrix.__len__() --> # rows
        # resistance_matrix[0].__len__() --> # columns
        if (resistance_matrix.__len__() != self.rows):
            raise Exception(f"Rows of resistance matrix not equal rows of crossbar!\nExpected number of rows: {str(self.rows)} \
                            Rows in the input matrix: {str(resistance_matrix.__len__())}")
        for matrix_row in resistance_matrix:
            if (matrix_row.__len__() != self.cols):
                raise Exception("Columns of resistance matrix in row {str(resistance_matrix.index(matrix_row))} \
                                not equal columns of crossbar!\nExpected number of columns: {str(self.cols)}. Columns in matrix row:  \
                                {str(matrix_row.__len__())}\nGiven matrix row: {str(matrix_row)}")
        [self.update_device(x, y, resistance_matrix[y][x]) for x in range(self.cols) for y in range(self.rows)]

    ###################################################################################
    def create_netlist(self):
        '''
        Create the crossbar netlist.
        If the the spice flag is not enabled, then no actual spice netlist will be created.
        In this case this function only initializes the values of the \"voltage sources\" to 1V
        that will be later used from other functions.
        '''
        # Set flag that the netlist has been created
        self.netlist_created = 1

        if self.spice:
            self.logger = Logging.setup_logging()
            self.circuit = Circuit(self.name)

            # Node 0 i think is ground
            # Generate sources
            for y in range(self.rows):
                self.circuit.V(str(y), y+1, self.circuit.gnd,
                               self.sources_values[y])
            # Setup devices:
            for y in range(self.rows):
                for x in range(self.cols):
                    id = self.devices[y][x].id
                    resistance = self.devices[y][x].R
                    self.circuit.R(id, y+1, self.read_node_str[x], resistance)
            utility.v_print_2(self.circuit)

            for x in range(self.cols):
                self.circuit.R(
                    "_read_"+str(x), self.read_node_str[x], self.circuit.gnd, self.R_read[x])

            regExR = r"R\d+"
            regExV = r"V\d+"
            regExRead = r"R_read"

            for element in self.circuit.elements:
                ch_str = element.name
                if re.match(regExR, ch_str):  # if the name start with R and is followed by number
                    self.res.append(element)
                if re.match(regExV, ch_str):  # if the name matches V and is followed by numbers
                    self.sources.append(element)
                if re.match(regExRead, ch_str):
                    self.read_res.append(element)

            for i in self.read_res:
                i.plus.add_current_probe(self.circuit)
        else:
            # No spice level netlist needs to be created, we just initialize the source vector that is used for other functions
            self.sources = [self.sources_values[y]
                            @ u_V for y in range(self.rows)]
            utility.v_print_1("Spice set to false, this function does nothing")

    ###################################################################################
    def circuit_solver(self):
        '''
        Run the spice simulation and calculate branch current and node voltages (DC static analysis)
        '''
        print("Spice Sim!")
        if (self.netlist_created == 1) and (self.spice):

            simulator = self.circuit.simulator(
                temperature=25, nominal_temperature=25)

            analysis = simulator.operating_point()
            for node in analysis.nodes.values():
                utility.v_print_2(
                    'Node {}: {} V'.format(str(node), float(node)))

            for branch in analysis.branches.values():
                utility.v_print_2("Branch: ", str(
                    branch), " A: ", float(branch))
                self.currents.append(branch)
        else:
            raise Exception(
                f"ERROR [circuit_solver {self.name}]! There is no defined netlist or spice simulation is not enabled!")

    ###################################################################################
    def sim(self):
        '''
        Run simulation for the netlist
        '''
        if self.spice:
            self.circuit_solver()
            return self.get_current()
        else:
            return self.fast_sim()
