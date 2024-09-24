LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE std.env.ALL;

ENTITY MIMO_TB IS

END MIMO_TB;

ARCHITECTURE sim OF MIMO_TB IS

  SIGNAL clk   : STD_LOGIC := '0';
  SIGNAL rst_n : STD_LOGIC := '0';
  SIGNAL start : STD_LOGIC := '0'; -- Start a single program and computer round
  SIGNAL done  : STD_LOGIC;
BEGIN

  -- TODO instantiate the proper module and pass the inputs  

  clk   <= NOT clk AFTER 5 ns;
  rst_n <= '1' AFTER 3 ns;
  start <= '1' AFTER 10 ns;
  P_reg : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
    ELSIF rising_edge(clk) THEN
      IF (done = '1') THEN
        stop;
      END IF;
    END IF;
  END PROCESS;

END sim;