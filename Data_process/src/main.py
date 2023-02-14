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


def check_file_pattern(filename):
    filename_pattern = r'^.*(?P<row>r\d+).*(?P<column>c_\d+).*(?P<iteration>rep_\d+)\.csv.*$'

    match = re.match(filename_pattern, filename)

    if match:
        row = int(match.group('row')[1:]) if match.group('row') else None
        column = int(match.group('column')[2:]) if match.group('column') else None
        iteration = int(match.group('iteration')[4:]) if match.group('iteration') else None
        # print(f'row={row}, column={column}, iteration={iteration}')
        return [int(row), int(column), int(iteration)]
    else:
        print('Filename does not match pattern')
        return False


def read_Data(filename):
    print(filename)
    return 0


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
    args = parser.parse_args()
    return args


def main():
    args = read_arg()
    path = args.path
    if not os.path.isdir(path):
        raise Exception("The path is not a directory")

    same = 0
    temp = 0
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            x = check_file_pattern(filename)
            if x:
                print(x)
                # check if the two files have the same number of rows
                if x[0] == temp:
                    same = 1
                else:
                    same = 0
                    temp = x[0]

                if (x[0] == 1000):
                    if same == 1:
                        print("same")
                        df1 = pd.read_csv(filepath)
                        dfm = pd.merge(df, df1)
                        print(df1)
                        print("dfm")
                        print(dfm)
                    else:
                        df = pd.read_csv(filepath)
                        print(df)


if __name__ == "__main__":
    main()
