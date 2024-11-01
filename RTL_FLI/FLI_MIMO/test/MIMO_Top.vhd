LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE std.env.ALL;

ENTITY MIMO_TB IS

END MIMO_TB;

ARCHITECTURE sim OF MIMO_TB IS

  SIGNAL clk           : STD_LOGIC := '0';
  SIGNAL rst_n         : STD_LOGIC := '0';
  SIGNAL instr         : INSTRUCTION;
  SIGNAL data_in_comp  : int_array_ty(crossbar_rows - 1 DOWNTO 0);
  SIGNAL data_in_prog  : int_array_ty(crossbar_cols - 1 DOWNTO 0);
  SIGNAL cross_rdy     : STD_LOGIC;
  SIGNAL data_output   : int_array_ty(crossbar_cols - 1 DOWNTO 0);
  SIGNAL reading_prog  : STD_LOGIC;
  SIGNAL compute_cross : STD_LOGIC;
  SIGNAL valid         : STD_LOGIC;
BEGIN

  front_end_mem_inst : ENTITY work.front_end_mem
    PORT MAP(
      clk           => clk,
      rst_n         => rst_n,
      instr         => instr,
      data_in_comp  => data_in_comp,
      data_in_prog  => data_in_prog,
      cross_rdy     => cross_rdy,
      data_output   => data_output,
      reading_prog  => reading_prog,
      compute_cross => compute_cross,
      valid         => valid
    );

  clk   <= NOT clk AFTER 5 ns;
  rst_n <= '1' AFTER 3 ns;
END sim;