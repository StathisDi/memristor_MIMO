# Tool Chain instructions

## Using the crossbar simulator (Simbrain) 

### Requirements

* python==3.8
* cuda==11.6
* pytorch==1.13.1
* matplotlib

### Setting the environment

Before running simulations with the Python memristor crossbar you need to set an environment variable to point to the simbrain source directory. That is the directory that includes the simbrain directory and the .json files that define the technology parameters.

The environment variable should be named as `SIMBRAIN_PATH`.

### Simulating the crossbar

The pytorch-based simulation framework is accessed through an interface located in `MemMIMO/examples/MIMO/wrapper.py`.

This interface supports two types of operations: program and compute. For the program operation, the crossbar is programmed with memristor conductances that are modulated according to the matrix values. For the compute operation, the crossbar is read by applying readout voltage pulses to each row. The readout voltage pulses are generated according to the vector values.

The program function takes a matrix as input and returns 0 or 1. The compute function takes a vector as input and returns the result of the matrix-vector multiplication (MVM).

#### Crossbar settings

The `wrapper.py` statically defines the parameters of the crossbar. If you like to change the crossbar, you first need to edit the `wrapper.py` file.

Possible crossbar parameters:
| Parameter name      | Value       | Possible values                                                     |Notes|
|---------------------|-------------|---------------------------------------------------------------------|-----|
| CRB_ROW             | 3           | Integer                                                             | This value has to be the same in the C FLI interface |
| CRB_COL             | 2           | Integer                                                             | This value has to be the same in the C FLI interface |
| memristor_structure | "mimo"      | "mimo"                                                              | Should not be changed |
| memristor_device    | "new_ferro" | ideal, ferro, new_ferro, or hu                                      ||
| c2c_variation       | False       | True, False                                                         ||
| d2d_variation       | 0           | 0: No d2d variation, 1: both, 2: Gon/Goff only, 3: nonlinearity only||
| stuck_at_fault      | False       | True, False                                                         | Not used |
| retention_loss      | 0           | retention loss, 0: without it, 1: during pulse                      | Not used |
| aging_effect        | 0           | 0: No aging effect, 1: equation 1, 2: equation 2                    | Not used |

Parameters for the Peripheral Circuit
| Parameter name        | Value       | Possible values                                                             |Notes|
|-----------------------|-------------|-----------------------------------------------------------------------------|-----|
| wire_width            | 200         | Float                                                                       | In practice, wire_width shall be set around 1/2 of the memristor size; Hu: 10um; Ferro:200nm; |
| input_bit             | 8           | Integer                                                                     | This value has to much the HDL |
| CMOS_technode         | 14          | Integer                                                                     ||
| ADC_precision         | 32          | Integer                                                                     ||
| ADC_setting           | 4           | 2:two memristor crossbars use one ADC; 4:one memristor crossbar use one ADC ||
| ADC_rounding_function | "floor"     | floor or round                                                              ||
| device_roadmap        | "HP"        | HP: High Performance or LP: Low Power                                       ||
| temperature           | 300         | Integer                                                                     ||
| hardware_estimation   | True        | area and power estimation                                                   ||

## Compile and use of the FLI interface

This section explains how to compile and use the FLI interface for the memristor crossbar with Questasim.

### Requirements

To simulate the Python crossbar and VHDL front-end you require to have:
1) a c++ compiler
2) the foreign language interface (FLI) libraries from Questasim. The file name is mti.h and it is located to `<Questasim installation path>/include`
3) the python 3 c++ interface library. This is located in `<Python installation path>/include`
4) Set the appropriate values for rows and columns. The same value for the size of the crossbar need to be set for all languages. That includes the VHDL, MTI_frontend, and wrapper.py.

### How to compile the C++ interface for mix language simulation

Before compiling the code you need to set the path to the python crossbar in the MTI_frontend.cpp. The PY_PATH should point to the folder that includes the wrapper.py file.

#### Compile in windows

To compile for windows you can use the `CompileFLI.ps1` powershell script. The script can automatically compile and generate the .dll file that Questasim requires simulate the together with the Python crossbar. 

To use the script you need to define the proper paths for the Python and Questasim installation. You can also use the -help option for more details on how to use the script.

Example: 

1. `.\CompileFLI.ps1 -QSPath 'C:\custom\path\to\modelsim' -PyPath 'C:\custom\path\to\python' -Compiler 'C:\path\to\compiler\cl.exe' -SrcFile 'my_custom_file.cpp'"`

2. If you create a make folder inside the FLI_MIMO folder and considering that the paths are the same as the default paths in the CompileFLI.ps1 script, running the following command inside the `make` folder using powershell to create the necessary files:

`..\..\CompileFLI.ps1 -SrcFile ../src_c/MTI_frontend.cpp -Func initForeign -Out MTI_frontend.dll -Py`

#### Compile in linux

In linux you can compile to get .so file using gcc. You need to link the Questasim MTI and Python libraries.

#### Running the simulation using Questasim

To run the simulation in Questasim you need to copy the generated .dll, or .so, file to the folder with the project or where you run the simulation. 

You can also use the simulation.do script provided. There you can specify the location where the .so or .dll file is located. The .do script will automatically copy the file to the current directory and start the simulation. Note that the script does not compile the RTL, it assumes that the work library is already loaded in Questasim.

### Configure FLI C and RTL front-end

#### Configuring the RTL

In the `constants.vhd` set the following two parameters to match the ones in `wrapper.py`:
- `crossbar_rows` = `CRB_ROW`
- `crossbar_cols` = `CRB_COL`

You need to change these values and make sure they match, before compiling and simulating the RTL.

The RTL also attempts to emulate the crossbar programming and computation delay, and synchronize everything with the clock. This is done using two parameters in the `constants.vhd` package. The two variables (`prog_delay`, `comp_delay`) are set to constant values (50ns for programming and 20ns for computation) to make it easier to run and test the simulation. A more accurate behavior simulation can be implemented by using the following equations to calculate the delay:

- programming_time                  : TIME := (device_states - 1) * crossbar_rows * dt;
- computation_time                 : TIME := bitwidth * dt;

These times can be reduced by the number of clock cycles that the FSM takes to assemble the data. This is 1 clock cycle for the computation, and a number of cycles equal to the number of rows for the programming. That optimization can be made under the assumption that FSM ideally will send the data to program the crossbar row by row, while the python model operates over the full array.

Optimized values:
  - prog_delay = programming_time - period * (crossbar_rows)
  - comp_delay = computation_time - period

#### Configuring the FLI C

In the MTI format you need to define the following compiler constants:
- `PY_PATH` = Path to the folder containing the `wrapper.py`
- `CRB_COL` = must match the value set in the `wrapper.py`  
- `CRB_ROW` = must match the value set in the `wrapper.py` 

You do not need to edit the file to set these constants, alternatively you can set the values in your OS before the compilation process.

#### Programming the crossbar

The VHDL currently is using integer as inputs. The python corssbar simulator currently accepts inputs (real) from -1 to 1.
The mapping in this version is done by directly normalizing the values to -1 to 1. This mapping can be changed by altering the
mapping functions in the `util.h` file.

#### Changing the design

If the design is to be edited and the structure change, then the MTI_frontend needs to be edited as well to make sure that the correct signals are read from the C code.

That can be done by editing the line 301 to 312 in the `MTI_frontend.cpp` file. The name of the signals should follow the hierarchy of the design implemented. 

### Running an simulation

The current design includes a basic testbench that allows the user to implement a very simple simulation of the crossbar design together with its digital interface.

The testbench runs a simple program compute cycle that programs the crossbar design and the sends in a test vector that is used as input to the crossbar.

The testbench is implemented inside the `MIMO_Top.vhd` file, in the `RTL/test` folder.

To run the testbench the library file (`.dll` or `.so`). Once the file is created the `simulation.do` file can be used in Questasim to run the simulation.

Take note, that the correct paths need to be set inside the simulation.do file that points to the compiled library. Specifically the `source_path` should point to the location of the library file, and the `file_name` should hold the name of the library file.

Currently the device type is set to MF. The type can be changed by changing the type in the `wrapper.py` and generating a new device package for the VHDL.

The current design is using a 3 rows and 2 columns, that can also be changed by editing the `constants.vhd` and `wrapper.py` files accordingly. Take note that the values in those two files must match.

#### Changing the simulation environment

If the simulation environment changes and a different testbench is to be used,the  `simulation.do` file must be edited accordingly.

The following variables must be set:

- set source_path "C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_MIMO/make"
- set file_name "MTI_frontend.dll"
- set top_name "work.MIMO_TB"

The device type can be changed by changing the type in the `wrapper.py` and generating a new device package for the VHDL.

# LICENSE

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
