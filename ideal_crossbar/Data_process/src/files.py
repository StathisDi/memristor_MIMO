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


def read_n_rename_cols(filename, c, c_n):
    '''
    # Read a file an rename the error columns according to the exp iteration
    '''
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
