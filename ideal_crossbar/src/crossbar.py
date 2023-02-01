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
import random
import re
from utility import utility


# 1 Class for the Crossbar
#   Is build as a spice netlist using pyspice
#   Comprises from resistances in a nxm crossbar, where the n is the input rows and m the output
#   Has a solver
class crossbar:

    ###################################################################################
    # Constructor
    def __init__(self, name="", rows=0, cols=0, R_read=None, R_read_var=None):
        utility.v_print_1("Creating crossbar!\n")
        self.name = name
        self.rows = rows
        self.cols = cols
        self.inputs = rows
        self.outputs = cols
        self.elements = rows*cols
        self.devices = [[memristor(rows, cols, 'ideal', 0, 1@u_pΩ, 10000@u_MΩ) for x in range(cols)] for y in range(rows)]
        self.device_state = [[self.devices[y][x].R for x in range(cols)] for y in range(rows)]
        self.sources_values = [1@u_V for y in range(rows)]
        self.I_outputs = [0@u_A for x in range(cols)]
        self.netlist_created = 0
        self.res = []
        self.read_res = []
        self.sources = []
        self.currents = []
        self.voltages = []
        self.read_node_str = [str(x)+"_grd" for x in range(cols)]
        utility.v_print_2("Read_nodes: \n", self.read_node_str, "\n")

        if R_read_var == None:
            self.R_read_var = [0 for x in range(cols)]
            utility.v_print_1("R variations is not defined, 0% variations will be used!")
        else:
            self.R_read_var = R_read_var

        if not (any((0 <= x <= 1) for x in self.R_read_var)):
            raise Exception("R read variations should be in range [0,1]!")

        if R_read == None:
            self.R_read = [0.0000000000000000000001@u_pΩ for x in range(cols)]
            utility.v_print_1("R_read is not defined, 0.0000000000000000000001 pΩ value will be used!")
        else:  # assign values to R read including variation
            self.R_read = [(r+r*random.uniform(0, x)) for x in self.R_read_var for r in R_read]

        utility.v_print_1("\n\nInitialization of the crossbar setup completed!\n\n")

    ###################################################################################
    # to text function
    def __str__(self):
        return f"{self.name}: rows:{self.rows}, cols:{self.cols}, elements:{self.elements}"

    ###################################################################################
    # update the type of all devices in the crossbar
    def update_device_type(self, device='ideal', percentage_var=0,  Ron=1@u_kΩ, Roff=1000@u_kΩ, relative_sigma=0, absolute_sigma=0):
        for r in self.devices:
            for i in r:
                i.set_device_type(device, percentage_var, Ron, Roff, relative_sigma, absolute_sigma)

    ###################################################################################
    # Print the coordinates of each device
    def print_device_coordinates(self):
        for y in range(self.rows):
            for x in range(self.cols):
                print(self.devices[y][x].coordinates, "=", self.device[y][x].resistance, end=" ")
            print("")

    ###################################################################################
    # Detail print of the netlist, sources and resistances
    def print_netlist(self):
        if self.netlist_created == 1:
            for y in range(self.rows):
                print(self.sources[y], end=" --> ")
                for x in range(self.cols):
                    print(self.res[y*self.cols+x].resistance, end=" ")
                print("")
            print("Read resistances: ")
            [print(self.read_res[x]) for x in range(self.cols)]
            print(self.circuit)
        else:
            raise Exception("Netlist has not been created!")

    ###################################################################################
    # Detail print
    def detail_print(self):
        print(self.name, ":")
        print("\t Rows: ", self.rows)
        print("\t Columns: ", self.cols)
        print("\t Inputs: ", self.rows)
        print("\t Outputs: ", self.cols)
        print("\t Elements: ", self.elements)
        print("\t Device state: ")
        for y in range(self.rows):
            print(self.device_state[y])
        print("\t Sources:")
        print(self.sources_values)
        print("\t Current output:")
        print(self.I_outputs)

    ###################################################################################
    # Set source values.
    def set_sources(self, v):
        self.sources_values = v
        if (self.sources.__len__() != v.__len__()):
            raise Exception("Input vector of sources, not equal size as the number of sources!")

        if self.netlist_created == 1:
            for y in range(self.rows):
                self.sources[y].dc_value = v[y]
            utility.v_print_1("Netlist is updated!")
        else:
            utility.v_print_1("Source values are updated, waiting to create netlist!")

    ###################################################################################
    # Print the circuit sources
    def print_sources(self):
        if self.netlist_created == 1:
            print("Defined sources in the circuit: ", self.circuit.title)
            for source in self.sources:
                print(source)
        else:
            print("There is no netlist created!")

    ###################################################################################
    # Get current values per branch
    def get_current(self):
        # The first row currents are from the sources (negative), the rest are from the resistors
        # The name conventions (i.e. str format) is Branch vr0_plus for resistors and v9 for sources
        self.I_outputs = [i[0] for i in self.currents if re.match(r"vr", i._name)]
        [utility.v_print_2("Name: ", str(i), " Value: ", float(i)) for i in self.currents]
        utility.v_print_1("Calculated outputs:")
        utility.v_print_1(self.I_outputs)
        # TODO return on the double?
        return self.I_outputs
        # self.I_outputs = [0@u_A for x in range(self.cols)]  # Zero out currents
        # for i in self.currents:
        #    print("Name: ", str(i), " Value: ", float(i))]
        #    if re.match(r"vr", i._name):  # only consider the branches with resistors
        #        id = int(re.findall(r"\d{1,}", i._name)[0])  # Get the id of the resistor
        #        for x in range(self.cols):
        #            if (id % self.cols) == x:
        #                utility.v_print_2("id: ", id, " x is: ", x)
        #                self.I_outputs[x] += i[0]
        #            # sum = sum + i[0]  # Sum over the resistor currents

    ###################################################################################
    # Update device
    # Updates the internal state of a device in node [y,x] with a given resistance.
    # It updates the memristor element and the spice netlist
    def update_device(self, x, y, target_resistance):
        utility.v_print_1("Updating device resistance. Device: [", y, ",", x, "]")
        if not ((0 <= y < self.rows) and (0 <= x <= self.cols)):
            raise Exception("Try to access device with out of bounds coordinates.\nGiven coordinates: [" +
                            str(y)+","+str(x)+"]. Valid coordinate range y: [0," +
                            str(self.rows-1)+"] range of x: [0,"+str(self.cols-1)+"]")
        self.devices[y][x].update_state(target_resistance)
        self.device_state[y][x] = self.devices[y][x].R
        index = y*self.cols+x  # Translate the 2D index to the vector index of the netlist
        if self.netlist_created == 1:
            self.res[index].resistance = self.devices[y][x].R
            utility.v_print_1("Resistances in netlist is updated!")
        else:
            utility.v_print_1("Resistance values are updated, waiting to create netlist!")

    ###################################################################################
    # Updated all devices
    def update_all_devices(self, resistance_matrix):
        # resistance_matrix.__len__() --> # rows
        # resistance_matrix[0].__len__() --> # columns
        if (resistance_matrix.__len__() != self.rows):
            raise Exception("Rows of resistance matrix not equal rows of crossbar!\nExpected number of rows: " +
                            str(self.rows) + " Rows in the input matrix: " + str(resistance_matrix.__len__()))
        for matrix_row in resistance_matrix:
            if (matrix_row.__len__() != self.cols):
                raise Exception("Columns of resistance matrix in row "+str(resistance_matrix.index(matrix_row)) +
                                " not equal columns of crossbar!\nExpected number of columns: "+str(self.cols)+". Columns in matrix row:  " +
                                str(matrix_row.__len__())+"\nGiven matrix row: "+str(matrix_row))
        [self.update_device(x, y, resistance_matrix[y][x]) for x in range(self.cols) for y in range(self.rows)]

    ###################################################################################
    # Create the crossbar netlist
    def create_netlist(self):
        # Set flag that the netlist has been created
        self.netlist_created = 1
        self.logger = Logging.setup_logging()

        self.circuit = Circuit(self.name)

        # Node 0 i think is ground
        # Generate sources
        for y in range(self.rows):
            self.circuit.V(str(y), y+1, self.circuit.gnd, self.sources_values[y])
        # Setup devices:
        for y in range(self.rows):
            for x in range(self.cols):
                id = self.devices[y][x].id
                resistance = self.devices[y][x].R
                self.circuit.R(id, y+1, self.read_node_str[x], resistance)
        utility.v_print_1(self.circuit)

        for x in range(self.cols):
            self.circuit.R("_read_"+str(x), self.read_node_str[x], self.circuit.gnd, self.R_read[x])

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
        # for i in self.res:
        #    i.plus.add_current_probe(self.circuit)

    ###################################################################################
    # Calculate branch current and node voltages (DC static analysis)
    def circuit_solver(self):
        if self.netlist_created == 1:

            simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)

            analysis = simulator.operating_point()
            for node in analysis.nodes.values():
                utility.v_print_2('Node {}: {} V'.format(str(node), float(node)))

            for branch in analysis.branches.values():
                utility.v_print_2("Branch: ", str(branch), " A: ", float(branch))
                self.currents.append(branch)
        else:
            raise Exception("ERROR [circuit_solver ", self.name, " ]! There is no defined netlist!")
