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
from PySpice.Unit import u_Ω, u_A, u_V


def main():
    util = utility(2)
    cross = crossbar("Test crossbar", 2, 2)
    cross.create_netlist()
    cross.update_all_devices([[1@u_Ω, 1/2@u_Ω], [1/4@u_Ω, 1/5@u_Ω]])
    cross.print_netlist()
    cross.circuit_solver()
    o_current = cross.get_current()
    print("Read currents: \n", o_current)
    # try:
    #    cross.set_sources([20@u_V, 20@u_V, 20@u_V, 20@u_V, 20@u_V, 20@u_V])
    # except Exception as E:
    #    print(E)
    # cross.print_sources()
    # cross.circuit_solver()


if __name__ == "__main__":
    main()
