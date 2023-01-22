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

from PySpice.Unit import *
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_MΩ, u_pΩ
from utility import utility


# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage
class memristor:
    devices = 0

    def __init__(self, rows=-1, cols=-1, Ron=1@u_Ω, Roff=1000@u_Ω):
        self.id = memristor.devices
        if (rows != -1 or cols != -1):
            self.coordinates = (self.id//cols, self.id % cols)
        else:
            raise Exception("Number of Rows and Columns must be defined!")
        self.Ron = Ron
        self.Roff = Roff
        self.R = 1@u_Ω
        memristor.devices += 1

    def __str__(self):
        return f"ID:{self.id}, Ron:{self.Ron}, Roff:{self.Roff}, R:{self.R}, Location:{self.coordinates}"

    def update_state(self, resistance):
        # TODO add variation here
        if self.Ron <= resistance <= self.Roff:
            self.R = resistance
        else:
            raise Exception("Resistance programmed outside of [Ron, Roff] range!")
