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
    """ This function takes input the name of a file and checks if it fits the pattern.

        Returns:
            topple with the number of rows [0], columns [1] and experiment [2].
    """
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


def read_n_rename_cols(filename, c, c_n):
    df = pd.read_csv(filename)
    for i in range(0, c_n):
        df = df.rename(columns={str(i): str(i+c)})
    return df


def read_all_files(path, max_i, r):
    '''
    Read all files inside a directory and return a dictionary 
    '''
    temp = 0
    columns = 0
    columns_new = 0
    merge_df = None
    concat_df = None
    check = True
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            x = check_file_pattern(filename)
            if x and x[2] <= max_i:
                # check if the two files have the same number of rows
                if x[0] == temp:
                    # continue of experiments (same # rows)
                    columns += columns_new
                else:
                    # new sets of experiments (different # rows)
                    columns = 0
                    temp = x[0]

                columns_new = x[1]
                # When specified number of rows go through the files and compile one dataframe
                if (x[0] in r) or (0 in r):
                    print(f'{x} columns start from {columns}')
                    df = read_n_rename_cols(filepath, columns, columns_new)
                    merge_df = df if x[2] == 0 else pd.merge(merge_df, df)
                    if max_i == x[2]:
                        merge_df = merge_df.assign(rows=x[0])
                        concat_df = merge_df if (concat_df is None) else pd.concat([concat_df, merge_df], ignore_index=True)
                    check = False

    if check:
        raise Exception("No files read, check --r parameter.")

    return concat_df


def main():
    args = read_arg()
    path = args[0]
    max_i = args[1]
    r = args[2]
    try:
        df = read_all_files(path, max_i, r)
    except Exception as e:
        print(e)
        return (-1)

    print(f'Files read!:\n {df}')
    # Process function


if __name__ == "__main__":
    main()
