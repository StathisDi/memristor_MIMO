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
import pathlib
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
    parser.add_argument("-c", "--config_file", help="Configuration file", type=pathlib.Path, required=True)
    parser.add_argument("-v", "--verbose", help="Verbose level, 0-none, 1-level 1, 2-level 2", type=int, choices=[0, 1, 2], default=0)
    parser.add_argument("-g", "--gpu", help="GPU execution of matrix operations [boolean]", type=bool, default=False)
    parser.add_argument("-t", "--type", help="Experiment type, 0-variation (spice), 1-variation (fast) , 2-spice sim verification, 3-fast sim verification",
                        type=int, choices=[0, 1, 2, 3], required=True)

    args = parser.parse_args()
    return args


def main():
    args = read_arg()
    config_file = args.config_file
    ver_lvl = args.verbose
    gpu = args.gpu
    type = int(args.type)
    util = utility(ver_lvl, gpu)
    config = configuration(config_file)
    Ron = config.Ron
    Roff = config.Roff
    # Fields in relative and absolute sigma ["start" - float, "inc" - float, "lim" - float, "mul" -  bool]
    # for 0 -> start -> start (+ or * depending on mul) incr -> up to lim
    sigma_relative = config.sigma_relative
    sigma_absolute = config.sigma_absolute
    # Fields in rows ["start" - int, "inc" - int, "lim" - int]
    # for start -> 0 + inc -> inc + inc -> up to lim
    rows = config.rows
    cols = config.cols
    rep = config.rep
    # Fields in logs ["path" -  string, "variations" - bool, "conductance" - bool]
    logs = config.logs
    del config
    utility.v_print_2(f"Type is {type}")
    utility.v_print_2(f"Ron is {Ron}")
    utility.v_print_2(f"Roff is {Roff}")
    utility.v_print_2(f"Sigma abs is {sigma_absolute}")
    utility.v_print_2(f"Sigma rel is {sigma_relative}")
    utility.v_print_2(f"Rows is {rows}")
    utility.v_print_2(f"Cols are {cols}")
    utility.v_print_2(f"Rep is {rep}")
    utility.v_print_2(f"Logs are {logs}")
    if type == 0:
        utility.v_print_1(f"Variation experiment - spice")
        variation_tb(Ron, Roff, 0, 3, sigma_absolute, sigma_relative, rep, rows, cols, logs, True)
    elif type == 1:
        utility.v_print_1(f'Variation experiment - Fast sim')
        variation_tb(Ron, Roff, 0, 3, sigma_absolute, sigma_relative, rep, rows, cols, logs, False)
    elif type == 2:
        utility.v_print_1(f"Verification process for the spice sim")
        verification_tb(False, rep)
    elif type == 3:
        utility.v_print_1(f"Verification process for the fast sim")
        verification_tb(True, rep)


if __name__ == "__main__":
    main()
