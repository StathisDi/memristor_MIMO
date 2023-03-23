#!python3.7

#
# Author : Dimitrios Stathis
# Copyright 2022
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

# Configuration class that is used in the compilation.py

import json


class configuration:
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

        self.rows = self.read_attribute("rows", 10)
        self.rows_inc = self.read_attribute("rows_inc", 250)
        self.rows_lim = self.read_attribute("rows_lim", 500)
        self.cols = self.read_attribute("cols", 750)
        self.rep = self.read_attribute("rep", 10)
        self.sigma_absolute = self.read_attribute("sigma_absolute", 0.0)
        self.sigma_relative = self.read_attribute("sigma_relative", 0.0)
        self.relative_increment = self.read_attribute("relative_increment", 0.1)
