""" 
MIT License

Copyright (c) 2024 Dimitrios Stathis

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

import os
import argparse
import pickle
import vhdl_codegen as hdl

def get_file_path_from_args():
    """Parse the file path from command-line arguments and validate if the file exists."""
    parser = argparse.ArgumentParser(description="Process a file path.")
    parser.add_argument('file_path', type=str, help='The path to the file.')
    parser.add_argument('-o', type=str, help='Output file name (without extension).', default='device_config_pkg')
    args = parser.parse_args()

    # Validate if the file exists
    if os.path.isfile(args.file_path):
        print(f"File found: {args.file_path}")
        return args
    else:
        # Raise custom exception if the file doesn't exist
        raise FileNotFoundError(f"Error: The file '{args.file_path}' does not exist.")

'''
Write out the VHDL package=>
inputs:
device_data: dictionary with the device data
o: the name of the output file
'''
def write_package(device_data, name, o):
    # Create a VHDL package
    pkg = hdl.VHDLPackage(o)

    pkg.add_library("IEEE")
    pkg.add_use_clause("IEEE.std_logic_1164.ALL")
    pkg.add_use_clause("IEEE.math_real.ALL")

    pkg.add_constant("device_type", str("\""+str(name)+"\""), "string")
    pkg.add_constant("device_states", device_data.get('total_no'), "integer")
    pkg.add_constant("dt", "{:.10f}".format(device_data.get('cycle:')), "time")
    pkg.add_constant("duty_cycle", device_data.get('duty ratio'), "real")

    code_gen = hdl.VHDLCodeGen()
    code_gen.add_package(pkg)
    print(code_gen)
    code_gen.write_to_file(o+'.vhd')

def main():

    try:
        args = get_file_path_from_args()
    except FileNotFoundError as e:
        print(e)
        exit(-1)
    pkl = args.file_path
    o_name = args.o
    # total_no => states
    # voltage => write voltage 
    # cycle => dt (pulse/clock cycle)
    # duty ratio => duty cycle
    # V_reset => reset voltage
    # conductance => LUT from minimum conductance to max conductance 
    with open(pkl, 'rb') as f:
        data = pickle.load(f)
    print('Devices found in file:')
    for k in data.keys():
        print("- "+k)
    select = input("Select device [string]\n")
    if (select not in data.keys()):
        raise SystemExit("Device selected not in file.")
    print("Device selected: ("+str(select)+") ")
    print(str(data.get(select)))
    write_package(data.get(select),select,o_name)


if __name__ == "__main__":
    main()