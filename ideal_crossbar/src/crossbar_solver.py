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

# Crossbar dimensions:
# Rows --> Input sources
# Columns --> Outputs during computation, ground during programming

# Calculation of Voltages depending on the state of the devices (R) and the Voltage sources

# 1 Main program that reads the above and simulates
from crossbar_n_device_class import crossbar


def main():
    cross = crossbar("Test crossbar", 3, 5)
    cross.detail_print()

    cross.create_netlist()
    cross.circuit_solver()
    # logger = Logging.setup_logging()

    # circuit = Circuit('Voltage Divider')

    # Node 0 i think is ground
    # circuit.V('input', 1, circuit.gnd, 10@u_V)
    # circuit.R(1, 1, 2, 15@u_Ω)
    # circuit.R(2, 2, circuit.gnd, 5@u_Ω)
    # circuit.R(3, 1, 3, 7.5@u_Ω)
    # circuit.R(4, 3, circuit.gnd, 2.5@u_Ω)
    # We can get an element or a model using its name using these two possibilities::
    # circuit['R1'] # dictionary style
    # circuit.R1    # attribute style
    # We can update an element parameter like this::
    # circuit.R1.resistance = kilo(1)
    # regEx = r"R\s*"
    # res = []
    # for element in circuit.elements:
    #    ch_str = element.name
    #    if re.match(regEx, ch_str):
    #        # print(ch_str)
    #        res.append(element)
    # for i in res:
    #    # print(i)
    #    i.plus.add_current_probe(circuit)
    # exit()
    # for resistance in (circuit.R1, circuit.R2):
    #    resistance.plus.add_current_probe(circuit)
    #    resistance.minus.add_current_probe(circuit)

    # simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    # analysis = simulator.operating_point()
    # for node in analysis.nodes.values():  # .in is invalid !
    #    print('Node {}: {} V'.format(str(node), float(node)))

    # for branch in analysis.branches.values():
    #    print('Branch {}: {} A'.format(str(branch), float(branch)))  # Fixme: format value + unit


if __name__ == "__main__":
    main()
