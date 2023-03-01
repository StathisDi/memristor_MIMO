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

import numpy as np
import sys
import argparse
import re
import pandas as pd
import os
from files import *
from plot import *
import matplotlib.pyplot as plt


def read_arg():
    parser = argparse.ArgumentParser(
        description="Script to process data from variation experiments.\n \
        It takes input the path to the folder where the csv files are stored.\n \
        The file names should have a format where the rows, columns and experiment run are specified.\n \
        the row filed should start with \'r\' (eg \'r40\' for 40 rows), the column should start with \'c_\'\n \
        and the experimental run with \'rep_\'.\n \
        Example : \'test_r40_c_30_rep_2.csv\'."
    )
    parser.add_argument("path", help="Path to folder where the csv files are located!")
    parser.add_argument("-m", "--max_iterations", dest="max", default="0", help="Read all files with iteration number equal or lower that this. Takes non-negative values.")
    parser.add_argument("-r", "--row", dest="row", type=int, nargs='+',
                        default=[0], help="Reads only files from experiments with a specific number of rows. It can take multiple values, if 0 then it reads all.")
    args = parser.parse_args()
    path = args.path
    if not os.path.isdir(path):
        raise Exception("The path is not a directory")
    max_i = int(args.max)
    if max_i < 0:
        raise Exception("Negative value given to -m parameter.")
    r = args.row
    for i in r:
        if i < 0:
            raise Exception("Negative value given to -r parameter.")
    return [path, max_i, r]


def main():
    args = read_arg()
    path = args[0]
    max_i = args[1]
    r = args[2]
    try:
        exp_df = read_all_files(path, max_i, r)
    except Exception as e:
        print(e)
        return (-1)

    print(f'Files read!:\n {exp_df}')
    # Process function
    plot_var_error(exp_df, 'abs')
    plot_var_error(exp_df, 'rel')
    plt.show()


if __name__ == "__main__":
    main()
