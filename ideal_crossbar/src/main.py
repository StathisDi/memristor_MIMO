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


#############################################################


def read_arg():
    parser = argparse.ArgumentParser(
        description="Python simulation for memristor crossbar (experiments with variations)"
    )
    parser.add_argument("rows", help="Initial number of rows.")
    parser.add_argument("cols", help="Upper limit number of rows.")
    parser.add_argument("rep", help="repetition.")
    parser.add_argument("sigma_absolute", help="Set values for sigma absolute")
    parser.add_argument("sigma_relative", help="Set values for sigma relative")

    args = parser.parse_args()
    return args


def main():
    util = utility(0)
    args = read_arg()
    # verification_tb()
    Ron = 1.0e3  # in kOhm
    Roff = 1.0e6  # in kOhm
    sigma_relative = 0.02438171519582677
    sigma_absolute = 0.005490197724238527
    sigma_relative = 0.1032073708277878
    sigma_absolute = 0.005783083695110348
    rows = int(args.rows)
    cols = int(args.cols)
    rep = int(args.rep)
    # sigma_absolute = float(args.sigma_absolute)
    # sigma_relative = float(args.sigma_relative)
    variation_tb(Ron, Roff, 0, 3, sigma_absolute, sigma_relative, rep, rows, cols)


if __name__ == "__main__":
    main()
