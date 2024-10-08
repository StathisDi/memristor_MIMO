# Memristor_MIMO

Experiments and simulation setup for MIMO in memory computation using memristors

# Requirements

## For crossbar

1) Python 3
2) PySpice

Installation instructions for python can be found [here](https://www.python.org/)!

Installation instructions for PySpice can be found [here](https://pyspice.fabrice-salvaire.fr/releases/v1.4/overview.html#how-to-install-pyspice)!

## For the data processing

1) [Pandas](https://github.com/pandas-dev/pandas)

## For RTL/FLI 

To co-simulate the crossbar implemented in python together with the RTL models of the digital side of the architecture we are using the FLI of Questasim/Modelsim.

To simulate the combined design you need Questasim/Modelsim, a c/c++ compiler and have python installed.

The scripts to compile the c+python model and simulate it together with the RTL model of the digital side in windows can be found in the **RTL_FLI** folder.

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
