LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;

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
END PACKAGE;