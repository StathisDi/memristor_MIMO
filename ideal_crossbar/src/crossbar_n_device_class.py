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
from PySpice.Unit import u_Ω, u_A, u_V
import numpy
import re
from utility import utility
# TODO add verbose statements

# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage


class memristor:
    devices = 0

    def __init__(self, rows=-1, cols=-1, Ron=1@u_Ω, Roff=1000@u_Ω):
        self.id = memristor.devices
        if (rows != -1 or cols != -1):
            self.coordinates = (self.id//cols, self.id % cols)
        else:
            raise Exception("Number of Rows and Columns must be defined!")
        self.Ron = Ron
        self.Roff = Roff
        self.R = 1@u_Ω
        memristor.devices += 1

    def __str__(self):
        return f"ID:{self.id}, Ron:{self.Ron}, Roff:{self.Roff}, R:{self.R}, Location:{self.coordinates}"

    def update_state(self, resistance):
        # TODO add variation here
        if self.Ron <= resistance <= self.Roff:
            self.R = resistance
        else:
            raise Exception("Resistance programmed outside of [Ron, Roff] range!")


# 1 Class for the Crossbar
#   Is build as a spice netlist using pyspice
#   Comprises from resistances in a nxm crossbar, where the n is the input rows and m the output
#   Has a solver
class crossbar:

    def __init__(self, name="", rows=0, cols=0):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.inputs = rows
        self.outputs = cols
        self.elements = rows*cols
        self.devices = [[memristor(rows, cols, 0@u_Ω, 10@u_Ω) for x in range(cols)] for y in range(rows)]
        self.device_state = [[self.devices[y][x].R for x in range(cols)] for y in range(rows)]
        self.sources_values = [1@u_V for y in range(rows)]
        self.I_outputs = [0@u_A for x in range(cols)]
        self.netlist_created = 0
        self.res = []
        self.sources = []
        self.currents = []
        self.voltages = []

    def __str__(self):
        return f"{self.name}: rows:{self.rows}, cols:{self.cols}, elements:{self.elements}"

    def print_device_coordinates(self):
        for y in range(self.rows):
            for x in range(self.cols):
                utility.v_print_1(self.devices[y][x].coordinates, end=" ")
            utility.v_print_1("")

    def print_netlist(self):
        if self.netlist_created == 1:
            for y in range(self.rows):
                utility.v_print_1(self.sources[y], end=" --> ")
                for x in range(self.cols):
                    utility.v_print_1(self.res[y*self.cols+x].resistance, end=" ")
                utility.v_print_1("")
            utility.v_print_1(self.circuit)
        else:
            raise Exception("Netlist has not been created!")

    def detail_print(self):
        utility.v_print_1(self.name, ":")
        utility.v_print_1("\t Rows: ", self.rows)
        utility.v_print_1("\t Columns: ", self.cols)
        utility.v_print_1("\t Inputs: ", self.rows)
        utility.v_print_1("\t Outputs: ", self.cols)
        utility.v_print_1("\t Elements: ", self.elements)
        utility.v_print_1("\t Device state: ")
        for y in range(self.rows):
            utility.v_print_1(self.device_state[y])
        utility.v_print_1("\t Sources:")
        utility.v_print_1(self.sources_values)
        utility.v_print_1("\t Current output:")
        utility.v_print_1(self.I_outputs)

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

    # Print the circuit sources
    def print_sources(self):
        if self.netlist_created == 1:
            utility.v_print_1("Defined sources in the circuit: ", self.circuit.title)
            for source in self.sources:
                utility.v_print_1(source)
        else:
            utility.v_print_1("There is no netlist created!")

    # Get current values per branch
    def get_current(self):
        # The first row currents are from the sources (negative), the rest are from the resistors
        # The name conventions (i.e. str format) is Branch vr0_plus for resistors and v9 for sources
        sum = 0.0@u_A
        for i in self.currents:
            print('Branch {}: {} A'.format(str(i), float(i)))
            if re.match(r"vr", i._name):  # only consider the branches with resistors
                id = int(re.findall(r"\d{1,}", i._name)[0])  # Get the id of the resistor
                # TODO filter and sum the resistors that add to one "branch"
                sum = sum + i[0]  # Sum over the resistor currents
        print(sum)

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
                self.circuit.R(id, y+1, self.circuit.gnd, resistance)
        utility.v_print_1(self.circuit)

        regExR = r"R\d*"
        regExV = r"V\d*"

        for element in self.circuit.elements:
            ch_str = element.name
            if re.match(regExR, ch_str):  # if the name start with R and is followed by number
                self.res.append(element)
            if re.match(regExV, ch_str):  # if the name matches V and is followed by numbers
                self.sources.append(element)

        for i in self.res:
            i.plus.add_current_probe(self.circuit)

    # Solve the circuit
    def circuit_solver(self):
        if self.netlist_created == 1:

            simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)

            analysis = simulator.operating_point()
            for node in analysis.nodes.values():
                utility.v_print_1('Node {}: {} V'.format(str(node), float(node)))

            for branch in analysis.branches.values():
                self.currents.append(branch)
        else:
            raise Exception("ERROR [circuit_solver ", self.name, " ]! There is no defined netlist!")
