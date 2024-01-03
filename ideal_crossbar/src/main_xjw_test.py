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
from testbenches import *
from configuration_class import configuration

#############################################################

def main():
    _Ron = 1.0e3  # in kOhm
    _Roff = 1.0e6  # in kOhm
    _V_min = 0.0
    _V_max = 3.0
    _var_rel = 0 
    _var_abs = 0
    _rep = 1
    _rows = 10
    _cols = 4
    _logs=['test_data', None, False, False, None]

    _crossbar = crossbar("Test crossbar fast", _rows, _cols, False)
    run_fast_sim(_crossbar, _Ron, _Roff, _V_min, _V_max, _var_rel, _var_abs, _rep, _rows, _cols, _logs)

if __name__ == "__main__":
    main()
