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

# Main script for testing functionality of the memristor class

from memristor import memristor
from utility import utility
from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_MΩ, as_Ω
import pint


def main():
    # u = pint.UnitRegistry()
    # resistance_1 = 10@u_kΩ
    # resistance_2 = 100@u_Ω
    # resistance = resistance_2 + resistance_1
    # resistance = u_kΩ(resistance)
    # print(resistance)
    util = utility(2)
    mem = memristor(1, 1, 'ideal')
    mem.set_device_type('MF/SI')
    print(mem)
    target = 1000@u_MΩ
    mem.update_state(target)
    print(mem)
    difference = (as_Ω(mem.R) - target)
    # print(as_Ω(mem.R))
    print(u_kΩ(difference))
    mem.set_device_type('custom', 0.1, 1@u_kΩ, 1000@u_kΩ)
    print(mem)


if __name__ == "__main__":
    main()
