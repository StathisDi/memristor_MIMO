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

import csv
import os
import gc

# Class with utility functions


class utility:
    verbosity = 0

    def __init__(self, verb=-1):
        if (0 <= verb <= 2):
            utility.verbosity = verb
        else:
            raise Exception("Verbosity level can take values 0, 1, or 2!")

    #############################################################

    # Level 1 debug messages
    def v_print_1(*args, **kwargs):
        if utility.verbosity >= 1:
            print(*args, **kwargs)

    #############################################################

    # Level 2 debug messages
    def v_print_2(*args, **kwargs):
        if utility.verbosity >= 2:
            print(*args, **kwargs)

    #############################################################

    # calculate average of vector
    def cal_average(num):
        sum_num = 0
        for t in num:
            sum_num = sum_num + t

        avg = sum_num / len(num)
        return avg

    #############################################################

    # Compare and calculate error between values of two vectors
    # Raise Exception if passes a delta
    def compare(reference, modeled, delta):
        error = reference - modeled
        if any(abs(x) > delta for x in error):
            print("Reference:\n", reference)
            print("Modeled: \n", modeled)
            raise Exception("Large error: \n", error)
        return error

    #############################################################

    # Calculate error between values of two vectors
    # Does not raise Exception
    def cal_error(reference, modeled):
        error = reference - modeled
        return error

    #############################################################

    def translate_input(input, scale):
        # TODO translate a number to the resistance
        r = input*scale
        return r

    #############################################################

    def translate_output(input, scale):
        # TODO translate current to number
        num = input/scale
        return num

    #############################################################

    def write_to_csv(path_to_file=None, file_name=None, data=None):
        if file_name == None:
            raise Exception("Write to CSV requires parameter \"file_name\"!")
        if data == None:
            raise Exception("Write to CSV requires parameter \"data\"!")
        if path_to_file == None:
            raise Exception("Write to CSV requires parameter \"data\"!")
        if not (os.path.isdir(path_to_file)):
            raise Exception("Path given not valid!")
        file = path_to_file+"\\"+file_name
        utility.v_print_2("Path given = ", file)
        with open(file, 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(data)
            csv_writer = None
            f.close()
        gc.collect()
