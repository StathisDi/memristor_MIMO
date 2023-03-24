#!python3.7

#
# Author : Dimitrios Stathis
# Copyright 2023
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Configuration class gets a json file as input

import json


class configuration:

    def read_loop_attribute(self, name, var_names, default_values):
        if name in self.config_data:
            if len(var_names) == len(default_values):
                list = []
                for var in var_names:
                    list.append(self.config_data[name][var])
                return list
            else:
                raise Exception(f"ERROR (configuration-json) Length of var_names and default values does not match!")
        else:
            print(f'No \'{name}\' has been defined in the configuration file.\nDefault values {default_values} is set.')
            return default_values

    def read_attribute(self, var_name, default_value):
        if var_name in self.config_data:
            return self.config_data.get(var_name)
        else:
            print(f'No \'{var_name}\' has been defined in the configuration file.\nDefault value {default_value} is set.')
            return default_value

    def __init__(self, file_path):
        # Get the configuration path and open the file
        self.file_path = file_path
        with open(self.file_path, "r") as config_file:
            self.config_data = json.load(config_file)
            config_file.close
        self.Ron = self.read_attribute("Ron", 1.0e3)
        self.Roff = self.read_attribute("Roff", 1.0e6)
        loop_attributes = ["start", "inc", "lim"]
        default_values = [10, 250, 500]
        self.rows = self.read_loop_attribute("rows", loop_attributes, default_values)
        self.cols = self.read_attribute("cols", 750)
        self.rep = self.read_attribute("rep", 10)
        loop_attributes = ["start", "inc", "lim", "mul"]
        default_values = [0.001, 0.1, 1, False]
        self.sigma_absolute = self.read_loop_attribute("sigma_absolute", loop_attributes, default_values)
        self.sigma_relative = self.read_loop_attribute("sigma_relative", loop_attributes, default_values)
