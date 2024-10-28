LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
use work.device_config_pkg.ALL;

PACKAGE constants IS

  CONSTANT BITWIDTH : NATURAL := 12; --! The bitwidth value should be the same as the resolution set in the python model, i.e.  ADC_precision

  CONSTANT crossbar_rows : NATURAL := 3;
  CONSTANT crossbar_cols  : NATURAL := 2;
  CONSTANT period : time := 10 ns; --! This defines the period in ns that the digital design will run at

  CONSTANT program_val   : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0) :=(
    (-1234, 20),  -- Row 0
    (111, -41),   -- Row 1
    (401, 3124)   -- Row 1
  );

  CONSTANT compute_val   : int_array_ty(crossbar_rows - 1 DOWNTO 0) := (21474, 21474, 21474);
  -- We assume that each row is programmed in a single action, but the simulator accepts as input the full 
  -- crossbar configuration.
  -- To properly calculate the delay that crossbar would take we assemble the data here into a 2D array,
  -- The array is build cycle by cycle, once all the data are assembled we send them to the python simulator
  -- and delay the execution of the VHDL for the theoretical time that it takes to program the crossbar - the number of clocks that
  -- it took to assemble the data.
  -- This delay will emulate the delay that is required by the crossbar to program the values in the devices
  CONSTANT programing_time                  : TIME := (device_states - 1) * crossbar_rows * dt;
  CONSTANT computation_time                 : TIME := bitwidth * dt;
  CONSTANT prog_delay                       : TIME := programing_time - period * crossbar_rows;
  CONSTANT comp_delay                       : TIME := computation_time - period;
END PACKAGE;