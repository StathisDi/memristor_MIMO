#!python3.7

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

# Code structure:
# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy
import re


class memristor:
    devices = 0

    def __init__(self, Ron=10, Roff=1000):
        self.id = memristor.devices
        self.Ron = Ron
        self.Roff = Roff
        self.R = numpy.random.uniform(self.Ron, self.Roff)
        memristor.devices += 1

    def __str__(self):
        return f"ID:{self.id}, Ron:{self.Ron}, Roff:{self.Roff}, R:{self.R}"

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
        self.devices = [[memristor(0, 10) for x in range(cols)] for y in range(rows)]
        self.device_state = [[self.devices[y][x].R for x in range(cols)] for y in range(rows)]

    def __str__(self):
        return f"{self.name}: rows:{self.rows}, cols:{self.cols}, elements:{self.elements}"

    def update_state(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.device_state[y][x] = self.devices[y][x].R

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

    # Create the crossbar netlist
    def create_netlist(self):
        self.logger = Logging.setup_logging()

        self.circuit = Circuit('Voltage Divider')

        # Node 0 i think is ground
        self.circuit.V('input', 1, self.circuit.gnd, 10@u_V)
        self.circuit.R(1, 1, 2, 15@u_Ω)
        self.circuit.R(2, 2, self.circuit.gnd, 5@u_Ω)
        self.circuit.R(3, 1, 3, 7.5@u_Ω)
        self.circuit.R(4, 3, self.circuit.gnd, 2.5@u_Ω)

    # Solve the circuit
    def circuit_solver(self):
        regEx = r"R\s*"
        res = []

        for element in self.circuit.elements:
            ch_str = element.name
            if re.match(regEx, ch_str):
                res.append(element)

        for i in res:
            i.plus.add_current_probe(self.circuit)

        simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)

        analysis = simulator.operating_point()
        for node in analysis.nodes.values():
            print('Node {}: {} V'.format(str(node), float(node)))

        for branch in analysis.branches.values():
            print('Branch {}: {} A'.format(str(branch), float(branch)))
