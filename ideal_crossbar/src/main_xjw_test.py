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

import argparse

from utility import utility
from testbenches import *
from configuration_class import configuration
from mapping import MimoMapping

#############################################################
parser = argparse.ArgumentParser()
parser.add_argument("--memristor_structure", type=str, default='mimo') # trace, mimo or crossbar 
parser.add_argument("--memristor_device", type=str, default='ferro') # ideal, ferro, or hu
parser.add_argument("--c2c_variation", type=bool, default=False)
parser.add_argument("--d2d_variation", type=int, default=0) # 0: No d2d variation, 1: both, 2: Gon/Goff only, 3: nonlinearity only
parser.add_argument("--stuck_at_fault", type=bool, default=False)
parser.add_argument("--retention_loss", type=int, default=0) # retention loss, 0: without it, 1: during pulse, 2: no pluse for a long time
parser.add_argument("--aging_effect", type=int, default=0) # 0: No aging effect, 1: equation 1, 2: equation 2
args = parser.parse_args()

def main():
    # _Ron = 1.0e3  # in kOhm
    # _Roff = 1.0e6  # in kOhm
    # _V_min = 0.0
    # _V_max = 3.0
    # _var_rel = 0 
    # _var_abs = 0
    # 
    # _rows = 10
    # _cols = 4
    # 

    # _crossbar = crossbar("Test crossbar fast", _rows, _cols, False)
    # run_fast_sim(_crossbar, _Ron, _Roff, _V_min, _V_max, _var_rel, _var_abs, _logs)

    batch_size = 1
    _rows = 10
    _cols = 4
    _rep = 1
    _logs=['test_data', None, False, False, None]

    mem_device = {'device_structure':args.memristor_structure, 'device_name': args.memristor_device,
                 'c2c_variation': args.c2c_variation, 'd2d_variation': args.d2d_variation,
                 'stuck_at_fault': args.stuck_at_fault, 'retention_loss': args.retention_loss,
                 'aging_effect': args.aging_effect}
    
    _crossbar = MimoMapping(mem_device=mem_device, shape=(_rows, _cols))
    run_fast_sim(_crossbar, _rep, _rows, _cols, _logs)

if __name__ == "__main__":
    main()
