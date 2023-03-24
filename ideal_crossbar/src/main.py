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
from vmm import vmm
import argparse
from crossbar import crossbar
from testbenches import *
from configuration_class import configuration

#############################################################


def read_arg():
    parser = argparse.ArgumentParser(
        description="Python simulation for memristor crossbar (experiments with variations)"
    )
    parser.add_argument("-c", "--config_file", help="Configuration file", type=str, required=True)
    parser.add_argument("-t", "--type", help="Experiment type, 0-variation, 1-spice sim verification, 2-fast sim verification", type=int, choices=[0, 1, 2], required=True)

    args = parser.parse_args()
    return args


def main():
    util = utility(0)
    args = read_arg()
    config_file = args.config_file
    type = int(args.type)
    config = configuration(config_file)
    Ron = config.Ron
    Roff = config.Roff
    sigma_relative = config.sigma_relative
    sigma_absolute = config.sigma_absolute
    rows = config.rows
    cols = config.cols
    rep = config.rep
    del config
    print(f"Type is {type}")
    print(f"Ron is {Ron}")
    print(f"Roff is {Roff}")
    print(f"sigma abs is {sigma_absolute}")
    print(f"sigma rel is {sigma_relative}")
    print(f"rows is {rows}")
    print(f"rep is {rep}")
    # if type == 0:
    #    variation_tb(Ron, Roff, 0, 3, sigma_absolute, sigma_relative, rep, rows, cols)
    # elif type == 1:
    #    verification_tb(False, rep)
    # else:
    #    verification_tb(True, rep)


if __name__ == "__main__":
    main()
