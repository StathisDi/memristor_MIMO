# Memristor_MIMO

Experiments and simulation setup for the precoding operation of MIMO in memory computation using memristors.

This repository contains two separate parts. The first is the memristor crossbar python simulator, that is added here as a module. The git repository for the python simulator exist and is maintained in a stand-alone repository https://github.com/JoyJXU/MemMIMO. The second part of this repository contains an RTL front-end that allows to interact with the python crossbar simulator using VHDL and the foreign language interface (FLI) that Questasim provides. The RTL can be used to implement a vector-matrix multiplication, where the matrix is programmed in the crossbar and then multiple vectors can be send to the crossbar to calculate the product of the two.

# Requirements

## For crossbar

1) Python 3

Installation instructions for python can be found [here](https://www.python.org/)!

## For the data processing

1) [Pandas](https://github.com/pandas-dev/pandas)

## For RTL/FLI 

To co-simulate the crossbar implemented in python together with the RTL models of the digital side of the architecture we are using the FLI of Questasim/Modelsim.

To simulate the combined design you need Questasim/Modelsim, a c/c++ compiler and have python installed.

The scripts to compile the c+python model and simulate it together with the RTL model of the digital side in windows can be found in the **RTL_FLI** folder.

# Documentation and instructions

In each directory of the repository there is a `README.md` file that includes guidelines on how to use the different tools, and also how to edit and modify them when needed. More specifically:

1) In the `modules\MemMIMO\` you will find the readme file that explains how to set up and use the python simulator.
2) In the `RTL_FLI` you will find instructions how to set up, compile and run a simulation of the RTL digital front-end.
3) In the `RTL_FLI\FLI_MIMO\` you will find a readme file with documentation of the RTL designs that is used for to interface with python simulator, and also instructions on how to modify them.

# LICENSE

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
