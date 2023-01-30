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
from PySpice.Unit import u_Ω, u_A, u_V, u_kΩ, u_MΩ, u_pΩ, u_S, as_Ω, as_S
from utility import utility
import random
import pint


# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage
class memristor:
    devices = 0
    u = pint.UnitRegistry()

    ###################################################################################
    def __init__(self, rows=-1, cols=-1, device='ideal', percentage_var=0, Ron=1@u_Ω, Roff=1@u_MΩ,  relative_sigma=0, absolute_sigma=0):

        self.id = memristor.devices
        if (rows != -1 or cols != -1):
            self.coordinates = (self.id//cols, self.id % cols)
        else:
            raise Exception("Number of Rows and Columns must be defined!")
        self.type = device
        self.set_device_type(device, percentage_var, Ron, Roff, relative_sigma, absolute_sigma)
        self.R = self.Ron
        self.R_range = self.Roff - self.Ron
        memristor.devices += 1

    ###################################################################################
    def __str__(self):
        return f"\n ID:{self.id}, Device type:{self.type}, Location:{self.coordinates},\n    Ron:{u_kΩ(self.Ron)}, Roff:{u_kΩ(self.Roff)}, R range:{u_kΩ(self.R_range)},\n    R:{u_kΩ(self.R)}, Relative sigma:{self.sigma_relative}, Absolute Sigma:{self.sigma_absolute}\n"

    ###################################################################################
    def update_state(self, resistance):
        if self.Ron <= resistance <= self.Roff:
            # self.R = resistance
            utility.v_print_2("Target resistance is: ", u_kΩ(resistance))
            target_conductance = as_S(1/resistance)
            self.R = as_Ω(self.add_variation(target_conductance))
        else:
            raise Exception("Resistance programmed outside of [Ron, Roff] range!")

    ###################################################################################
    # Setting properties for each device model
    def set_device_type(self, device='ideal', percentage_var=0,  Ron=1@u_kΩ, Roff=1000@u_kΩ, relative_sigma=0, absolute_sigma=0):
        '''
        Allowed values for parameters

        device:
          - 'ideal'
          - 'ferro'
          - 'MF/SI'
          - 'custom'

        percentage_var:
          - 0 to 0.1
        '''
        self.type = device
        if not (0 <= percentage_var <= 0.1):
            raise Exception("Constant percentage variation has to be between 0 and 0.1!\n   Given: ", percentage_var)
        utility.v_print_1("Setting device to ", self.type)
        if (device == 'ideal'):
            # Ideal Memristor parameters
            self.Ron = Ron
            self.Roff = Roff

            self.sigma_relative = 0
            self.sigma_absolute = 0

        elif (device == 'ferro'):
            Goff = 7.0e-8@u_S
            Gon = 9.0e-6@u_S

            self.Roff = as_Ω(1/Goff)
            self.Ron = as_Ω(1/Gon)

            self.sigma_relative = 0.1032073708277878
            self.sigma_absolute = 0.005783083695110348

        elif (device == 'MF/SI'):

            Goff = 2.5e-10@u_S
            Gon = 1.85e-9@u_S

            self.Ron = as_Ω(1/Gon)
            self.Roff = as_Ω(1/Goff)

            self.sigma_relative = 0.02438171519582677
            self.sigma_absolute = 0.005490197724238527

        elif (device == 'custom'):
            Ron_var = random.uniform(-percentage_var, percentage_var)
            Roff_var = random.uniform(-percentage_var, percentage_var)
            self.Roff = as_Ω(Roff+Roff*Roff_var)
            self.Ron = as_Ω(Ron+Ron*Ron_var)
            if self.Ron < 1@u_Ω:
                self.Ron = 1@u_Ω
            # Custom variation
            self.sigma_relative = relative_sigma
            self.sigma_absolute = absolute_sigma

        else:
            raise Exception("Device Not Exist!")

    ###################################################################################
    def add_variation(self, conductance):
        Gon = as_S(1/self.Ron)
        Goff = as_S(1/self.Roff)
        if (self.type == 'ideal'):
            # Ideal device without variations
            utility.v_print_1("Update rule \'ideal\'")
            return (1/conductance)
        else:
            utility.v_print_1("Update rule \'variations\'")
            # Map conductance to x
            x = (conductance - Goff) / (Gon - Goff)  # target percent of change from off state
            utility.v_print_2("Target conductance: ", conductance, " is mapped to ", x)

            # Add variation
            v_relative = random.gauss(0, self.sigma_relative)
            v_absolute = random.gauss(0, self.sigma_absolute)
            utility.v_print_2("v_relative: ", v_relative, " v_absolute: ", v_absolute)

            # non ideal 5 change
            x_nonideal = x + x * v_relative + v_absolute
            utility.v_print_2("x_nonideal is: ", x_nonideal)

            # Make sure that the non ideal value is inside the Gon & Goff limits of the device
            x_nonideal = max(min(1, x_nonideal), 0)

            # Calculate conductance based on the non ideal % change
            c_nonideal = as_S(Goff + (x_nonideal * (Gon - Goff)))
            utility.v_print_2("Calculated conductance is: ", c_nonideal)

            return (1/c_nonideal)  # @u_Ω
