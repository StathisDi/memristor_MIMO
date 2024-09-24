# RTL FLI front end

This is an RTL front end for the python crossbar simulator.

## Configuration

Before simulating make sure that you set the following:

1) The values in the `constants.vhd` file must be set to much the values in the python simulator, `wrapper.py`.
2) The values in the `device_config_pkg.vhd` should also be set correctly with the same values as the python simulator. To do that you can generate a new file using the `export_device_config_pkg.py` in the `util` folder. Make sure that you select the same device as the one selected in the  `wrapper.py`.