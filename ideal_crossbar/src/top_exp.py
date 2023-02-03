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

# We use this as the top because of the memory leakage issue with ngspice

import numpy as np
import sys
import argparse
import os
import subprocess


def read_arg():
    parser = argparse.ArgumentParser(
        description="Python simulation for memristor crossbar (experiments with variations)"
    )
    parser.add_argument("iterations", help="Number of iterations")
    parser.add_argument("max_rows", help="Upper limit number of rows.")
    parser.add_argument("init_rows", help="Initial rows.")
    parser.add_argument("step_rows", help="Increment of rows")
    args = parser.parse_args()
    return args


def main():
    args = read_arg()
    iterations = int(args.iterations)
    max_rows = int(args.max_rows)
    init_rows = int(args.init_rows)
    step_rows = int(args.step_rows)
    for i in range(iterations):
        for y in range(init_rows, max_rows, step_rows):
            for var_abs in np.arange(0, 0.01, 0.0001):
                for var_rel in np.arange(0, 0.15, 0.0005):
                    if y != 0:
                        print(i, " ", y, " ", var_abs, " ", var_rel)
                        command = 'python ./main.py ' + str(y) + ' ' + str(4) + ' ' + str(i) + ' ' + str(var_abs) + ' ' + str(var_rel)
                        subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
