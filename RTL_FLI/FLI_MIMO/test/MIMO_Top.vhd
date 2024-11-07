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
      data_output   => data_output,
      reading_prog  => reading_prog,
      compute_cross => compute_cross,
      valid         => valid
    );

  clk   <= NOT clk AFTER 5 ns;
  rst_n <= '1' AFTER 3 ns;

  Test_bench : PROCESS
  BEGIN
    WAIT FOR 20 ns;
    IF (reading_prog = '1' AND compute_cross = '1') THEN
      WAIT UNTIL (reading_prog = '0' AND compute_cross = '0');
    END IF;
    instr <= PROGRAM_INST;
    FOR i IN 0 TO crossbar_rows - 1 LOOP
      WAIT UNTIL rising_edge(clk);
      FOR j IN 0 TO crossbar_cols - 1 LOOP
        data_in_prog(j) <= program_val(i, j);
      END LOOP;
    END LOOP;
    WAIT UNTIL rising_edge(clk);
    data_in_prog <= (OTHERS => 0);
    IF reading_prog = '1' THEN
      instr <= IDLE_INST;
      WAIT UNTIL reading_prog = '0';
    END IF;
    WAIT UNTIL rising_edge(clk);
    IF (cross_rdy = '0') THEN
      WAIT UNTIL cross_rdy = '1';
    END IF;
    instr <= COMPUTE_INST;
    WAIT UNTIL rising_edge(clk);
    instr <= IDLE_INST;
    FOR i IN 0 TO crossbar_rows - 1 LOOP
      data_in_comp(i) <= compute_val(i);
    END LOOP;
    WAIT UNTIL rising_edge(clk);
    IF (compute_cross = '1') THEN
      WAIT UNTIL compute_cross = '0';
    END IF;
    data_in_comp <= (OTHERS => 0);
    WAIT UNTIL rising_edge(clk);
    WAIT UNTIL rising_edge(clk);
    stop;
  END PROCESS; -- Test_bench
END sim;