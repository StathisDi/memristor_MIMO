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
import random

# TODO change everything to Ohm instead of k or M

# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage


class memristor:
    devices = 0

    ###################################################################################
    def __init__(self, rows=-1, cols=-1, device='ideal', Ron=1@u_Ω, Roff=1@u_MΩ, relative_sigma=0, absolute_sigma=0):
        self.id = memristor.devices
        if (rows != -1 or cols != -1):
            self.coordinates = (self.id//cols, self.id % cols)
        else:
            raise Exception("Number of Rows and Columns must be defined!")

        self.set_device_type(device, Ron, Roff, relative_sigma, absolute_sigma)
        self.R = self.Ron
        memristor.devices += 1

    ###################################################################################
    def __str__(self):
        return f"ID:{self.id}, Ron:{self.Ron}, Roff:{self.Roff}, R:{self.R},\n Location:{self.coordinates}, Relative sigma:{self.sigma_relative}, Absolute Sigma:{self.sigma_absolute}"

    ###################################################################################
    def update_state(self, resistance):
        if self.Ron <= resistance <= self.Roff:
            # self.R = resistance
            utility.v_print_2("Target resistance is: ", resistance)
            self.R = self.add_variation(1/resistance)
        else:
            raise Exception("Resistance programmed outside of [Ron, Roff] range!")

    ###################################################################################
    def set_device_type(self, device='ideal', Ron=1@u_Ω, Roff=1000@u_Ω, relative_sigma=0, absolute_sigma=0):
        if (device == 'ideal'):
            # Ideal Memristor parameters
            # P_on = 1
            # P_off = 1
            # Gon = 100
            # Goff = 1000
            # alpha_on = 1
            # alpha_off = 1
            # v_on = -1
            # v_off = 1
            # k_on = -100
            # k_off = 100
            # delta_t = 1e-3
            # TODO fix the values
            self.Ron = 1@u_kΩ
            self.Roff = 100000@u_kΩ

            self.sigma_relative = 0
            self.sigma_absolute = 0

        elif (device == 'ferro'):
            # fer Memristor parameters
            # P_on = 1.8
            # P_off = 0.9
            Gon = 7.0e-8
            Goff = 9.0e-6
            # alpha_on = 5
            # alpha_off = 5
            # v_on = -2
            # v_off = 1.4
            # k_on = -737387387.39
            # k_off = 113513.51
            # delta_t = 1e-7
            self.Ron = 1/Gon@u_Ω
            self.Ron = 1/Goff@u_Ω

            self.sigma_relative = 0.1032073708277878
            self.sigma_absolute = 0.005783083695110348

        elif (device == 'MF/SI'):
            # MF/SI Memristor parameters
            # P_on = 0.65
            # P_off = 5
            Gon = 2.5e-10
            Goff = 1.85e-9
            # alpha_on = 5
            # alpha_off = 5
            # v_on = -2
            # v_off = 2
            # k_on = -3.36
            # k_off = 19.52
            # delta_t = 30*1e-3
            self.Ron = 1/Gon@u_Ω
            self.Ron = 1/Goff@u_Ω

            self.sigma_relative = 0.02438171519582677
            self.sigma_absolute = 0.005490197724238527

        elif (device == 'Custom'):
            self.Ron = 1/Gon@u_Ω
            self.Ron = 1/Goff@u_Ω
            # Custom variation
            self.sigma_relative = relative_sigma
            self.sigma_absolute = absolute_sigma

        else:
            raise Exception("Device Not Exist!")

    ###################################################################################
    # TODO check the relationship between Gon, Goff, Ron, Roff and target and why there is a negative value
    def add_variation(self, conductance):

        Gon = 1/self.Ron
        Goff = 1/self.Roff
        # Map conductance to x
        x = (conductance - Gon) / (Goff - Gon)  # Gon and Goff are defined according to the memristor parameters
        utility.v_print_2("Target conductance: ", conductance, " is mapped to ", x)

        # Add variation
        v_relative = random.gauss(0, self.sigma_relative)
        v_absolute = random.gauss(0, self.sigma_absolute)

        x_nonideal = x + x * v_relative + v_absolute
        utility.v_print_2("x_nonideal is: ", x_nonideal)

        # Map x to conductance
        c_nonideal = (Gon + x_nonideal) * (Gon - Goff)
        utility.v_print_2("Calculated conductance is: ", c_nonideal)

        return 1/c_nonideal@u_Ω
