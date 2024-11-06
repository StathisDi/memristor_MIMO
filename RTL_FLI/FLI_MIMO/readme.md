# RTL FLI front end

This is an RTL front end for the python crossbar simulator.

## MIMO Control FSM

### Overview

The Control FSM for the memristor MIMO system is responsible for managing the programming and computation operations of the crossbar. It implements the timing and sequencing of these operations.

### Instructions

The FSM can receive the following types of instructions:
- **IDLE_INST**: No operation is performed.
- **PROGRAM_INST**: Programs the crossbar with the provided data.
- **COMPUTE_INST**: Performs computation using the crossbar with the provided data.

### FSM States

The FSM operates in the following states:
- **IDLE**: The default state where the FSM waits for an instruction. It transitions to the PROG state if a PROGRAM_INST is received and the crossbar is ready, or to the COMP state if a COMPUTE_INST is received and the crossbar is ready.
- **PROG**: The state where the FSM assembles and programs the crossbar with the provided data. It transitions back to the IDLE state once all rows have been assembled and programmed.
- **COMP**: The state where the FSM performs computation using the crossbar. It transitions back to the IDLE state once the computation is completed.

### Conditions

- The FSM transitions from IDLE to PROG or COMP only if the crossbar is ready (crossbar_rdy = '1').
- In the PROG state, the FSM assembles the programming data row by row and transitions back to IDLE once all rows are assembled and programmed. This is based on the delay set in the constants package.
- In the COMP state, the FSM performs the computation and transitions back to IDLE once the computation is done.  This is based on the delay set in the constants package.
- The FSM uses delays (prog_delay and comp_delay) to emulate the time required for programming and computation operations.

### Output Signals

| Signal Name         | Direction | Type                       | Description                                                                                           |
|---------------------|-----------|----------------------------|-------------------------------------------------------------------------------------------------------|
| cross_compute_data  | OUT       | int_array_ty               | Data sent to the crossbar for computation. This is a 1D array with the same number of elements as the rows in the crossbar. |
| cross_program_data  | OUT       | int_2d_array_ty            | Data sent to the crossbar for programming. This is a 2D array with dimensions matching the rows and columns of the crossbar. |
| reading_prog        | OUT       | STD_LOGIC                  | Asserted while programming the crossbar. During this time, it expects a new column of the crossbar in every cycle. |
| compute_cross       | OUT       | STD_LOGIC                  | Asserted while the computation is happening inside the crossbar. Deasserted when it is done. During the computation time, no new data should be sent to the crossbar. |
| program             | OUT       | STD_LOGIC                  | Control signal to program the crossbar.                                                               |
| compute             | OUT       | STD_LOGIC                  | Control signal to compute using the crossbar.                                                         |
| valid               | OUT       | STD_LOGIC                  | Asserted when the crossbar has completed the computation. It signals that the data is ready to be read. |

### Input Signals

| Signal Name        | Direction | Type            | Description                                                                                           |
|--------------------|-----------|-----------------|-------------------------------------------------------------------------------------------------------|
| instr              | IN        | INSTRUCTION     | Instruction signal indicating the operation to be performed (IDLE_INST, PROGRAM_INST, or COMPUTE_INST).|
| data_in_comp       | IN        | int_array_ty    | Data input for computation, provided as a 1D array equal to the number of rows in the crossbar.       |
| data_in_prog       | IN        | int_2d_array_ty | Data input for programming, provided as a 2D array with dimensions matching the rows and columns of the crossbar. |
| crossbar_rdy       | IN        | STD_LOGIC       | Signal indicating whether the crossbar is ready for programming or computation.                       |

## front_end_mem

### Overview

The `front_end_mem` entity combines the control FSM and the memristive crossbar. It emulates the timing required to program the crossbar and perform computations.

### Ports
| Port Name       | Direction | Description                                                                 |
|-----------------|-----------|-----------------------------------------------------------------------------|
| instr           | IN        | Instruction to be executed by the crossbar (of type `INSTRUCTION`).         |
| data_in_comp    | IN        | Data for computation, provided as a 1D array equal to the number of rows in the crossbar. |
| data_in_prog    | IN        | Data for programming the array, provided as a 1D array equal to the number of columns in the crossbar. |
| data_output     | OUT       | Output data from the crossbar, provided as a 1D array equal to the number of columns in the crossbar. |
| reading_prog    | OUT       | Asserted while programming the crossbar.                                    |
| compute_cross   | OUT       | Asserted while computation is happening inside the crossbar.                |
| valid           | OUT       | Asserted when the crossbar has completed the computation.                   |

### Components

| Component Name | Description |
|----------------|-------------|
| `mti_front`    | Component for interfacing with the C-defined architecture. |
| `MIMO_Control_FSM` | FSM for controlling the programming and computation operations. |


### Processes

- **P_comb**: Process that converts the real output of the crossbar to integer values for `data_output`.

### Usage

The `front_end_mem` entity is used to interface with the memristive crossbar, providing control signals and handling data input/output for programming and computation operations. The FSM ensures the correct sequencing and timing of these operations, based on the delays defined in the `constants` package.

## MIMO_TB

### Overview

The `MIMO_TB` entity is a testbench designed to verify the functionality of the `front_end_mem` entity, which interfaces with the memristive crossbar. It provides the necessary signals and sequences to test the programming and computation operations of the crossbar.

### Functionality

The `MIMO_TB` testbench performs the following operations:

1. Initializes the clock and reset signals.
2. Waits for the crossbar to be ready for programming.
3. Sends a `PROGRAM_INST` instruction and provides the programming data row by row.
4. Waits for the programming to complete and then sends an `IDLE_INST` instruction.
5. Waits for the crossbar to be ready for computation.
6. Sends a `COMPUTE_INST` instruction and provides the computation data.
7. Waits for the computation to complete and then sends an `IDLE_INST` instruction.
8. Stops the simulation after verifying the output data.

## Configuration

Before simulating make sure that you set the following:

1) The values in the `constants.vhd` file must be set to much the values in the python simulator, `wrapper.py`.
2) The values in the `device_config_pkg.vhd` should also be set correctly with the same values as the python simulator. To do that you can generate a new file using the `export_device_config_pkg.py` in the `util` folder. Make sure that you select the same device as the one selected in the  `wrapper.py`.