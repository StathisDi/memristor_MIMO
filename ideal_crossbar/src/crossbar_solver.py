# Crossbar dimensions:
# Rows --> Input sources
# Columns --> Outputs during computation, ground during programming

# Calculation of Voltages depending on the state of the devices (R) and the Voltage sources

# 1 Main program that reads the above and simulates
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy

# Code structure:
# 1 Class for the device (memristor):
#   Has: State, solver, and other device properties, input is the voltage


class memristor:
    devices = 0

    def __init__(self, Ron=10, Roff=1000):
        self.id = memristor.devices
        self.Ron = Ron
        self.Roff = Roff
        self.R = numpy.random.uniform(self.Ron, self.Roff)
        memristor.devices += 1

    def __str__(self):
        return f"ID:{self.id}, Ron:{self.Ron}, Roff:{self.Roff}, R:{self.R}"

# 1 Class for the Crossbar
#   Is build as a spice netlist using pyspice
#   Comprises from resistances in a nxm crossbar, where the n is the input rows and m the output
#   Has a solver


class crossbar:

    def __init__(self, name="", rows=0, cols=0):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.inputs = rows
        self.outputs = cols
        self.elements = rows*cols
        self.devices = [[memristor(0, 10) for x in range(cols)] for y in range(rows)]
        self.device_state = [[self.devices[y][x].R for x in range(cols)] for y in range(rows)]

    def __str__(self):
        return f"{self.name}: rows:{self.rows}, cols:{self.cols}, elements:{self.elements}"

    def update_state(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.device_state[y][x] = self.devices[y][x].R

    def detail_print(self):
        print(self.name, ":")
        print("\t Rows: ", self.rows)
        print("\t Columns: ", self.cols)
        print("\t Inputs: ", self.rows)
        print("\t Outputs: ", self.cols)
        print("\t Elements: ", self.elements)
        print("\t Device state: ")
        for y in range(self.rows):
            print(self.device_state[y])


def main():
    cross = crossbar("Test crossbar", 3, 5)
    cross.detail_print()

    logger = Logging.setup_logging()

    circuit = Circuit('Voltage Divider')

    # Node 0 i think is ground
    circuit.V('input', 1, circuit.gnd, 10@u_V)
    circuit.R(1, 1, 2, 9@u_kΩ)
    circuit.R(2, 2, 3, 1@u_kΩ)
    circuit.R(3, 3, circuit.gnd, 2@u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    analysis = simulator.operating_point()
    for node in analysis.nodes.values():  # .in is invalid !
        print('Node {}: {} V'.format(str(node), float(node)))


if __name__ == "__main__":
    main()
